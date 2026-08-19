#include <windows.h>
#include <shlobj.h>
#include <shlwapi.h>
#include <thumbcache.h>
#include <string>
#include <ole2.h>

#pragma comment(lib, "shlwapi.lib")
#pragma comment(lib, "ole32.lib")

// {9F3A6E21-75C1-4B7E-8E2C-4E2F8D9A45C7}
static const CLSID CLSID_ApkIconHandler =
    { 0x9F3A6E21, 0x75C1, 0x4B7E, { 0x8E, 0x2C, 0x4E, 0x2F, 0x8D, 0x9A, 0x45, 0xC7 } };

static HMODULE g_hModule = nullptr;

static std::wstring GetIconPath()
{
    wchar_t buf[MAX_PATH] = {};
    GetModuleFileNameW(g_hModule, buf, MAX_PATH);
    PathRemoveFileSpecW(buf);
    wcscat_s(buf, L"\\icon.ico");
    return buf;
}

static bool IsApkFile(LPCWSTR path)
{
    if (!path) return false;
    return PathMatchSpecW(path, L"*.apk") ||
           PathMatchSpecW(path, L"*.xapk") ||
           PathMatchSpecW(path, L"*.apks") ||
           PathMatchSpecW(path, L"*.apkm") ||
           PathMatchSpecW(path, L"*.aab");
}

class ApkIconHandler : public IExtractIconW, public IPersistFile, public IQueryInfo,
                       public IThumbnailProvider, public IInitializeWithFile
{
public:
    ApkIconHandler() : m_ref(1) {}
    virtual ~ApkIconHandler() {}

    STDMETHODIMP QueryInterface(REFIID riid, void** ppv)
    {
        *ppv = nullptr;
        if (IsEqualIID(riid, IID_IUnknown) || IsEqualIID(riid, IID_IExtractIconW))
            *ppv = static_cast<IExtractIconW*>(this);
        else if (IsEqualIID(riid, IID_IPersistFile))
            *ppv = static_cast<IPersistFile*>(this);
        else if (IsEqualIID(riid, IID_IQueryInfo))
            *ppv = static_cast<IQueryInfo*>(this);
        else if (IsEqualIID(riid, __uuidof(IThumbnailProvider)))
            *ppv = static_cast<IThumbnailProvider*>(this);
        else if (IsEqualIID(riid, __uuidof(IInitializeWithFile)))
            *ppv = static_cast<IInitializeWithFile*>(this);
        else
            return E_NOINTERFACE;
        AddRef();
        return S_OK;
    }
    STDMETHODIMP_(ULONG) AddRef() { return InterlockedIncrement(&m_ref); }
    STDMETHODIMP_(ULONG) Release()
    {
        ULONG r = InterlockedDecrement(&m_ref);
        if (r == 0) delete this;
        return r;
    }

    // IPersistFile
    STDMETHODIMP GetClassID(CLSID* pClassID) { *pClassID = CLSID_ApkIconHandler; return S_OK; }
    STDMETHODIMP IsDirty() { return S_FALSE; }
    STDMETHODIMP Load(LPCOLESTR pszFileName, DWORD) { m_path = pszFileName ? pszFileName : L""; return S_OK; }
    STDMETHODIMP Save(LPCOLESTR, BOOL) { return E_NOTIMPL; }
    STDMETHODIMP SaveCompleted(LPCOLESTR) { return E_NOTIMPL; }
    STDMETHODIMP GetCurFile(LPOLESTR*) { return E_NOTIMPL; }

    // IInitializeWithFile
    STDMETHODIMP Initialize(LPCWSTR pszFile, DWORD) { m_path = pszFile ? pszFile : L""; return S_OK; }

    // IExtractIconW
    STDMETHODIMP GetIconLocation(UINT, LPWSTR szIconFile, UINT cchMax, int* piIndex, UINT* pwFlags)
    {
        *pwFlags = GIL_DONTCACHE | GIL_PERINSTANCE;
        *piIndex = 0;
        if (m_path.empty() || !IsApkFile(m_path.c_str()))
            return S_FALSE;
        std::wstring ico = GetIconPath();
        if (GetFileAttributesW(ico.c_str()) == INVALID_FILE_ATTRIBUTES)
            return S_FALSE;
        if (szIconFile && cchMax > 0)
            wcsncpy_s(szIconFile, cchMax, ico.c_str(), _TRUNCATE);
        return S_OK;
    }

    STDMETHODIMP Extract(LPCWSTR pszFile, UINT, HICON* phiconLarge, HICON* phiconSmall, UINT nIconSize)
    {
        if (phiconLarge) *phiconLarge = nullptr;
        if (phiconSmall) *phiconSmall = nullptr;
        std::wstring apk = pszFile ? pszFile : m_path;
        if (apk.empty() || !IsApkFile(apk.c_str()))
            return S_FALSE;
        std::wstring ico = GetIconPath();
        if (GetFileAttributesW(ico.c_str()) == INVALID_FILE_ATTRIBUTES)
            return S_FALSE;
        int largeSize = (int)(nIconSize & 0xFFFF);
        int smallSize = (int)((nIconSize >> 16) & 0xFFFF);
        if (largeSize == 0) largeSize = 48;
        if (smallSize == 0) smallSize = 16;
        bool gotIcon = false;
        if (phiconLarge)
        {
            *phiconLarge = (HICON)LoadImageW(nullptr, ico.c_str(), IMAGE_ICON,
                largeSize, largeSize, LR_LOADFROMFILE | LR_DEFAULTCOLOR);
            if (*phiconLarge) gotIcon = true;
        }
        if (phiconSmall)
        {
            *phiconSmall = (HICON)LoadImageW(nullptr, ico.c_str(), IMAGE_ICON,
                smallSize, smallSize, LR_LOADFROMFILE | LR_DEFAULTCOLOR);
            if (*phiconSmall) gotIcon = true;
        }
        return gotIcon ? S_OK : S_FALSE;
    }

    // IQueryInfo
    STDMETHODIMP GetInfoTip(DWORD, wchar_t** ppwszTip)
    {
        if (!ppwszTip) return E_POINTER;
        *ppwszTip = nullptr;
        if (m_path.empty()) return S_FALSE;
        std::wstring tip = L"APK: " + m_path;
        *ppwszTip = (wchar_t*)CoTaskMemAlloc((tip.size() + 1) * sizeof(wchar_t));
        if (*ppwszTip) wcscpy_s(*ppwszTip, tip.size() + 1, tip.c_str());
        return S_OK;
    }
    STDMETHODIMP GetInfoFlags(DWORD* pdwFlags) { *pdwFlags = 0; return S_OK; }

    // IThumbnailProvider
    STDMETHODIMP GetThumbnail(UINT cx, HBITMAP* phbmp, WTS_ALPHATYPE* pdwAlpha)
    {
        if (!phbmp || !pdwAlpha) return E_POINTER;
        *phbmp = nullptr;
        *pdwAlpha = WTSAT_UNKNOWN;
        if (m_path.empty() || !IsApkFile(m_path.c_str()))
            return S_FALSE;
        std::wstring ico = GetIconPath();
        if (GetFileAttributesW(ico.c_str()) == INVALID_FILE_ATTRIBUTES)
            return S_FALSE;
        HICON hIcon = (HICON)LoadImageW(nullptr, ico.c_str(), IMAGE_ICON,
            cx, cx, LR_LOADFROMFILE | LR_DEFAULTCOLOR);
        if (!hIcon) return S_FALSE;
        HDC hdc = GetDC(nullptr);
        BITMAPINFO bmi = {};
        bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
        bmi.bmiHeader.biWidth = (LONG)cx;
        bmi.bmiHeader.biHeight = -(LONG)cx;
        bmi.bmiHeader.biPlanes = 1;
        bmi.bmiHeader.biBitCount = 32;
        bmi.bmiHeader.biCompression = BI_RGB;
        void* bits = nullptr;
        HBITMAP hbmp = CreateDIBSection(hdc, &bmi, DIB_RGB_COLORS, &bits, nullptr, 0);
        ReleaseDC(nullptr, hdc);
        if (!hbmp) { DestroyIcon(hIcon); return E_OUTOFMEMORY; }
        HDC hdcMem = CreateCompatibleDC(nullptr);
        if (hdcMem)
        {
            HBITMAP oldBmp = (HBITMAP)SelectObject(hdcMem, hbmp);
            RECT rc = { 0, 0, (LONG)cx, (LONG)cx };
            FillRect(hdcMem, &rc, (HBRUSH)GetStockObject(NULL_BRUSH));
            DrawIconEx(hdcMem, 0, 0, hIcon, cx, cx, 0, nullptr, DI_NORMAL);
            SelectObject(hdcMem, oldBmp);
            DeleteDC(hdcMem);
        }
        DestroyIcon(hIcon);
        *phbmp = hbmp;
        *pdwAlpha = WTSAT_ARGB;
        return S_OK;
    }

private:
    LONG m_ref;
    std::wstring m_path;
};

class ClassFactory : public IClassFactory
{
public:
    ClassFactory() : m_ref(1) {}
    STDMETHODIMP QueryInterface(REFIID riid, void** ppv)
    {
        if (IsEqualIID(riid, IID_IUnknown) || IsEqualIID(riid, IID_IClassFactory))
        { *ppv = static_cast<IClassFactory*>(this); AddRef(); return S_OK; }
        *ppv = nullptr; return E_NOINTERFACE;
    }
    STDMETHODIMP_(ULONG) AddRef() { return InterlockedIncrement(&m_ref); }
    STDMETHODIMP_(ULONG) Release() { ULONG r = InterlockedDecrement(&m_ref); if (r == 0) delete this; return r; }
    STDMETHODIMP CreateInstance(LPUNKNOWN pUnkOuter, REFIID riid, void** ppv)
    {
        if (pUnkOuter) return CLASS_E_NOAGGREGATION;
        ApkIconHandler* p = new ApkIconHandler();
        HRESULT hr = p->QueryInterface(riid, ppv);
        p->Release();
        return hr;
    }
    STDMETHODIMP LockServer(BOOL) { return S_OK; }
private:
    LONG m_ref;
};

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason, LPVOID)
{
    if (ul_reason == DLL_PROCESS_ATTACH)
    {
        g_hModule = hModule;
        DisableThreadLibraryCalls(hModule);
    }
    return TRUE;
}

extern "C" STDAPI DllGetClassObject(REFCLSID rclsid, REFIID riid, void** ppv)
{
    if (!IsEqualCLSID(rclsid, CLSID_ApkIconHandler)) return CLASS_E_CLASSNOTAVAILABLE;
    ClassFactory* cf = new ClassFactory();
    HRESULT hr = cf->QueryInterface(riid, ppv);
    cf->Release();
    return hr;
}

extern "C" STDAPI DllCanUnloadNow() { return S_OK; }

static const wchar_t* kCLSID = L"{9F3A6E21-75C1-4B7E-8E2C-4E2F8D9A45C7}";

extern "C" STDAPI DllRegisterServer()
{
    wchar_t dllPath[MAX_PATH];
    GetModuleFileNameW(g_hModule, dllPath, MAX_PATH);
    wchar_t key[256]; HKEY hKey;

    wsprintfW(key, L"CLSID\\%s", kCLSID);
    RegCreateKeyExW(HKEY_CLASSES_ROOT, key, 0, nullptr, 0, KEY_WRITE, nullptr, &hKey, nullptr);
    RegSetValueExW(hKey, nullptr, 0, REG_SZ, (BYTE*)L"WSA APK Icon", 26);
    wcscat_s(key, L"\\InprocServer32");
    RegCreateKeyExW(HKEY_CLASSES_ROOT, key, 0, nullptr, 0, KEY_WRITE, nullptr, &hKey, nullptr);
    RegSetValueExW(hKey, nullptr, 0, REG_SZ, (BYTE*)dllPath, (DWORD)(wcslen(dllPath)+1)*sizeof(wchar_t));
    RegSetValueExW(hKey, L"ThreadingModel", 0, REG_SZ, (BYTE*)L"Both", 8);

    wsprintfW(key, L".apk\\shellex\\IconHandler");
    RegCreateKeyExW(HKEY_CLASSES_ROOT, key, 0, nullptr, 0, KEY_WRITE, nullptr, &hKey, nullptr);
    RegSetValueExW(hKey, nullptr, 0, REG_SZ, (BYTE*)kCLSID, (DWORD)(wcslen(kCLSID)+1)*sizeof(wchar_t));

    wsprintfW(key, L".apk\\shellex\\{E357FCCD-A995-4576-B01F-234630154E96}");
    RegCreateKeyExW(HKEY_CLASSES_ROOT, key, 0, nullptr, 0, KEY_WRITE, nullptr, &hKey, nullptr);
    RegSetValueExW(hKey, nullptr, 0, REG_SZ, (BYTE*)kCLSID, (DWORD)(wcslen(kCLSID)+1)*sizeof(wchar_t));

    SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, nullptr, nullptr);
    return S_OK;
}

extern "C" STDAPI DllUnregisterServer()
{
    RegDeleteTreeW(HKEY_CLASSES_ROOT, L"CLSID\\{9F3A6E21-75C1-4B7E-8E2C-4E2F8D9A45C7}");
    RegDeleteTreeW(HKEY_CLASSES_ROOT, L".apk\\shellex\\IconHandler");
    RegDeleteTreeW(HKEY_CLASSES_ROOT, L".apk\\shellex\\{E357FCCD-A995-4576-B01F-234630154E96}");
    SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, nullptr, nullptr);
    return S_OK;
}
