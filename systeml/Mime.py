class Mime():
    def get_content_type(self, content_bytes = None, path = None, file_name = None, content = None):
        """Определяет MIME-тип по сигнатурам байтов, пути или имени файла"""
        
        # Читаем байты
        data = None
        if content_bytes:
            data = content_bytes[:4096]
        elif path:
            with open(path, "rb") as f:
                data = f.read(4096)

        if path:
            file_path = path
        else:
            file_path = file_name

        if data:
            # === ИЗОБРАЖЕНИЯ ===
            if data[:8] == b'\x89PNG\r\n\x1a\n':
                return "image/png"
            if data[:3] == b'\xff\xd8\xff':
                return "image/jpeg"
            if data[:6] in (b'GIF87a', b'GIF89a'):
                return "image/gif"
            if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
                return "image/webp"
            if data[:2] == b'BM':
                return "image/bmp"
            if data[:4] == b'\x00\x00\x01\x00':
                return "image/x-icon"
            if data[:4] == b'\x00\x00\x02\x00':
                return "image/x-cursor"
            if data[:12] == b'\x00\x00\x00\x0cjP  \r\n\x87\n':
                return "image/jp2"
            if data[:2] == b'II' or data[:2] == b'MM':
                return "image/tiff"
            if data[:4] == b'8BPS':
                return "image/vnd.adobe.photoshop"
            if data[:3] == b'\x00\x00\x00' and data[4:12] == b'ftypheic':
                return "image/heic"
            if data[:3] == b'\x00\x00\x00' and data[4:12] == b'ftypavif':
                return "image/avif"
            if data.startswith(b'gimp xcf'):
                return "image/x-xcf"
            if data[:4] == b'DDS ':
                return "image/vnd-ms.dds"
            
            # === ВИДЕО ===
            if data[4:8] == b'ftyp':
                ftyp_brand = data[8:12]
                if ftyp_brand in (b'mp42', b'mp41', b'isom', b'avc1', b'iso2'):
                    return "video/mp4"
                if ftyp_brand in (b'M4V ', b'M4VH', b'M4VP'):
                    return "video/x-m4v"
                if ftyp_brand == b'qt  ':
                    return "video/quicktime"
                if ftyp_brand in (b'3gp4', b'3gp5', b'3gp6'):
                    return "video/3gpp"
                if ftyp_brand == b'3g2a':
                    return "video/3gpp2"
                return "video/mp4"
            
            if data[:4] == b'\x1aE\xdf\xa3':
                return "video/x-matroska"
            if data[:3] == b'FLV':
                return "video/x-flv"
            if data[:4] == b'RIFF' and data[8:12] == b'AVI ':
                return "video/x-msvideo"
            if data[:8] == b'\x30\x26\xb2\x75\x8e\x66\xcf\x11':
                return "video/x-ms-wmv"
            if data[:4] == b'\x00\x00\x01\xba' or data[:4] == b'\x00\x00\x01\xb3':
                return "video/mpeg"
            
            # === АУДИО ===
            if data[:4] == b'RIFF' and data[8:12] == b'WAVE':
                return "audio/wav"
            if data[:3] == b'ID3' or data[:2] == b'\xff\xfb' or data[:2] == b'\xff\xf3' or data[:2] == b'\xff\xf2':
                return "audio/mpeg"
            if data[:4] == b'fLaC':
                return "audio/flac"
            if data[:4] == b'OggS':
                if b'vorbis' in data[:100]:
                    return "audio/ogg"
                if b'OpusHead' in data[:100]:
                    return "audio/opus"
                return "audio/ogg"
            if data[4:8] == b'ftyp' and data[8:12] in (b'M4A ', b'M4B ', b'mp42'):
                return "audio/mp4"
            if data[:4] == b'FORM' and data[8:12] == b'AIFF':
                return "audio/aiff"
            if data[:3] == b'MAC':
                return "audio/x-ape"
            if data[:4] == b'wvpk':
                return "audio/x-wavpack"
            if data[:4] == b'TTA1':
                return "audio/x-tta"
            
            # === АРХИВЫ ===
            if data[:2] == b'PK':
                if data[2:4] == b'\x03\x04':
                    if file_path:
                        ext = file_path.lower()
                        if ext.endswith('.docx'):
                            return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        if ext.endswith('.xlsx'):
                            return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        if ext.endswith('.pptx'):
                            return "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                        if ext.endswith('.odt'):
                            return "application/vnd.oasis.opendocument.text"
                        if ext.endswith('.ods'):
                            return "application/vnd.oasis.opendocument.spreadsheet"
                        if ext.endswith('.odp'):
                            return "application/vnd.oasis.opendocument.presentation"
                        if ext.endswith('.jar'):
                            return "application/java-archive"
                        if ext.endswith('.apk'):
                            return "application/vnd.android.package-archive"
                        if ext.endswith('.epub'):
                            return "application/epub+zip"
                    return "application/zip"
                if data[2:4] == b'\x05\x06' or data[2:4] == b'\x07\x08':
                    return "application/zip"
            
            if data[:4] == b'Rar!' or data[:8] == b'Rar!\x1a\x07\x01\x00':
                return "application/x-rar-compressed"
            if data[:6] == b'7z\xbc\xaf\x27\x1c':
                return "application/x-7z-compressed"
            if data[:3] == b'\x1f\x8b\x08':
                return "application/gzip"
            if data[:2] == b'BZ' and data[2:3] == b'h':
                return "application/x-bzip2"
            if data[:6] == b'\xfd7zXZ\x00':
                return "application/x-xz"
            if data[:4] == b'\x28\xb5\x2f\xfd':
                return "application/zstd"
            if data[:5] == b'ustar':
                return "application/x-tar"
            if data[:7] == b'\x89LZO\x00\r\n':
                return "application/x-lzop"
            if data[:4] == b'LZIP':
                return "application/x-lzip"
            if data[:3] == b'LZ4':
                return "application/x-lz4"
            if data[:4] == b'!<ar':
                return "application/x-archive"
            if data[:4] == b'\x1f\x9d\x90':
                return "application/x-compress"
            
            # === ДОКУМЕНТЫ ===
            if data[:4] == b'%PDF':
                return "application/pdf"
            if data[:8] == b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1':
                if file_path:
                    ext = file_path.lower()
                    if ext.endswith('.doc'):
                        return "application/msword"
                    if ext.endswith('.xls'):
                        return "application/vnd.ms-excel"
                    if ext.endswith('.ppt'):
                        return "application/vnd.ms-powerpoint"
                    if ext.endswith('.msg'):
                        return "application/vnd.ms-outlook"
                    if ext.endswith('.msi'):
                        return "application/x-msi"
                return "application/x-ole-storage"
            if data[:5] == b'{\\rtf':
                return "application/rtf"
            if data[:4] == b'\x09\x04\x06\x00' or data[:4] == b'\x09\x08\x10\x00':
                return "application/vnd.ms-excel"
            if data[:4] == b'\xd0\xcf\x11\xe0':
                return "application/msword"
            
            # === ИСПОЛНЯЕМЫЕ ===
            if data[:2] == b'MZ':
                return "application/x-msdownload"
            if data[:4] == b'\x7fELF':
                return "application/x-executable"
            if data[:4] == b'\xca\xfe\xba\xbe' or data[:4] == b'\xfe\xed\xfa\xce' or data[:4] == b'\xfe\xed\xfa\xcf':
                return "application/x-mach-binary"
            if data[:4] == b'\xcf\xfa\xed\xfe':
                return "application/x-mach-binary"
            if data[:2] == b'#!':
                return "text/x-shellscript"
            if data[:4] == b'\x00\x61\x73\x6d':
                return "application/wasm"
            if data[:4] == b'dex\n':
                return "application/x-dex"
            
            # === ШРИФТЫ ===
            if data[:4] == b'wOFF':
                return "font/woff"
            if data[:4] == b'wOF2':
                return "font/woff2"
            if data[:4] == b'\x00\x01\x00\x00' and file_path and file_path.endswith('.ttf'):
                return "font/ttf"
            if data[:4] == b'OTTO':
                return "font/otf"
            if data[:34] == b'\x00\x01\x00\x00\x00':
                return "font/ttf"
            if data[:4] == b'true':
                return "font/ttf"
            if data[:4] == b'ttcf':
                return "font/collection"
            
            # === БАЗЫ ДАННЫХ ===
            if data[:16] == b'SQLite format 3\x00':
                return "application/x-sqlite3"
            if data[:8] == b'\x00\x61\x73\x6d\x01\x00\x00\x00':
                return "application/wasm"
            if data[:4] == b'\xed\xab\xee\xdb':
                return "application/x-rpm"
            if data[:8] == b'\x53\x51\x4c\x69\x74\x65\x20\x66':
                return "application/x-sqlite3"
            
            # === CAD/3D ===
            if data[:6] == b'CATDRA':
                return "application/x-catia"
            if data[:4] == b'glTF':
                return "model/gltf-binary"
            if data[:4] == b'\x4d\x4d\x00\x2a' or data[:4] == b'\x49\x49\x2a\x00':
                return "image/tiff"
            if data.startswith(b'solid '):
                return "model/stl"
            if data[:5] == b'IGES\x00' or data[:80].startswith(b'                                                                                S      1'):
                return "model/iges"
            if data[:6] == b'AC1015' or data[:6] == b'AC1018' or data[:6] == b'AC1021' or data[:6] == b'AC1024' or data[:6] == b'AC1027' or data[:6] == b'AC1032':
                return "application/x-dwg"
            
            # === СПЕЦИАЛЬНЫЕ ФОРМАТЫ ===
            if data[:4] == b'\x50\x4b\x03\x04' and b'mimetype' in data[:100]:
                return "application/epub+zip"
            if data[:8] == b'CR24\x03\x02\x00\x00':
                return "image/x-canon-cr2"
            if data[:4] == b'II\x2a\x00' and data[8:18] == b'CR\x02\x00\x00\x00':
                return "image/x-canon-crw"
            if data[:4] == b'FORM':
                if data[8:12] == b'ILBM':
                    return "image/x-ilbm"
                if data[8:12] == b'AIFF':
                    return "audio/aiff"
            if data[:12] == b'BLENDER':
                return "application/x-blender"
            if data[:4] == b'PS-X':
                return "application/postscript"
            if data[:2] == b'%!' or data[:4] == b'%PDF':
                return "application/postscript"
            
            # === КОМПИЛЯТОРЫ/DEV ===
            if data[:4] == b'\x7fELF':
                return "application/x-object"
            if data[:8] == b'!<arch>\n':
                return "application/x-archive"
            if data[:4] == b'\xca\xfe\xba\xbe':
                return "application/java-vm"
            if data[:4] == b'\xfe\xed\xfa\xce':
                return "application/x-mach-binary"
            
            # === ДИСКИ/ОБРАЗЫ ===
            if data[:8] == b'EFIPART\x00':
                return "application/x-gpt"
            if data[510:512] == b'\x55\xaa':
                return "application/x-iso9660-image"
            if data[:32] == b'CD001':
                return "application/x-iso9660-image"
            if data[:7] == b'MSCF\x00\x00\x00':
                return "application/vnd.ms-cab-compressed"
            if data[:4] == b'KDMV':
                return "application/x-vmdk"
            if data[:8] == b'conectix' or data[:8] == b'cxsparse':
                return "application/x-vhd"
            if data[:7] == b'vhdxfile':
                return "application/x-vhdx"
            if data[:4] == b'QFI\xfb':
                return "application/x-qcow"
        
        if file_path:
            # === ТЕКСТОВЫЕ ФОРМАТЫ ===
            try:
                if content:
                    text_sample = content[:min(1024, len(content))]
                elif data:
                    text_sample = data[:1024].decode('utf-8', errors='ignore')
                else:
                    text_sample = ""
                
                # HTML
                if '<html' in text_sample.lower() or '<!doctype html' in text_sample.lower() or '<HTML' in text_sample:
                    return "text/html"
                
                # XML/SVG
                if text_sample.strip().startswith('<?xml'):
                    if file_path and file_path.endswith('.svg'):
                        return "image/svg+xml"
                    if '<svg' in text_sample.lower():
                        return "image/svg+xml"
                    return "application/xml"
                
                if text_sample.strip().startswith('<svg'):
                    return "image/svg+xml"
                
                # JSON
                stripped = text_sample.strip()
                if stripped.startswith(('{', '[')):
                    try:
                        import json
                        json.loads(text_sample[:512])
                        return "application/json"
                    except:
                        pass
                
                # YAML
                if file_path and file_path.endswith(('.yml', '.yaml')):
                    return "text/yaml"
                
                # CSS
                if file_path and file_path.endswith('.css'):
                    return "text/css"
                
                # JavaScript/TypeScript
                if file_path:
                    if file_path.endswith(('.js', '.mjs', '.cjs')):
                        return "application/javascript"
                    if file_path.endswith('.ts'):
                        return "application/typescript"
                    if file_path.endswith('.jsx'):
                        return "text/jsx"
                    if file_path.endswith('.tsx'):
                        return "text/tsx"
                
                # Markdown
                if file_path and file_path.endswith(('.md', '.markdown')):
                    return "text/markdown"
                
                # CSV/TSV
                if file_path:
                    if file_path.endswith('.csv'):
                        return "text/csv"
                    if file_path.endswith('.tsv'):
                        return "text/tab-separated-values"
                
                # Конфиги
                if file_path:
                    if file_path.endswith('.ini'):
                        return "text/plain"
                    if file_path.endswith('.conf'):
                        return "text/plain"
                    if file_path.endswith('.toml'):
                        return "application/toml"
                
                # Языки программирования
                if file_path:
                    if file_path.endswith('.py'):
                        return "text/x-python"
                    if file_path.endswith(('.c', '.h')):
                        return "text/x-c"
                    if file_path.endswith(('.cpp', '.cc', '.cxx', '.hpp')):
                        return "text/x-c++"
                    if file_path.endswith('.java'):
                        return "text/x-java"
                    if file_path.endswith('.rs'):
                        return "text/x-rust"
                    if file_path.endswith('.go'):
                        return "text/x-go"
                    if file_path.endswith('.rb'):
                        return "text/x-ruby"
                    if file_path.endswith('.php'):
                        return "application/x-php"
                    if file_path.endswith('.sh'):
                        return "text/x-shellscript"
                    if file_path.endswith('.bat'):
                        return "application/bat"
                    if file_path.endswith('.ps1'):
                        return "application/x-powershell"
                
                # Обычный текст
                return "text/plain"
            
            except UnicodeDecodeError:
                pass
        
        # === ДЕФОЛТ ===
        return "application/octet-stream"