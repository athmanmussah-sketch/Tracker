#!/usr/bin/python
# DARKX TOOL - ADVANCED TRACKER
# “Wahai orang-orang yang beriman! Janganlah kamu saling memakan harta sesamamu dengan jalan yang batil,” (QS. An Nisaa': 29). 
# Rasulullah SAW juga melarang umatnya untuk mengambil hak orang lain tanpa izin.

import json
import requests
import time
import os
import phonenumbers
import re
import socket
from phonenumbers import carrier, geocoder, timezone
from sys import stderr
from urllib.parse import urlparse

# Colors
Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'

# utilities
def is_option(func):
    def wrapper(*args, **kwargs):
        run_banner()
        func(*args, **kwargs)
    return wrapper

# ---------- TRACKING FUNCTIONS ----------

@is_option
def IP_Track():
    ip = input(f"{Wh}\n Enter IP target : {Gr}")
    print()
    print(f' {Wh}============= {Gr}IP ADDRESS INFORMATION {Wh}=============')
    try:
        req_api = requests.get(f"http://ipwho.is/{ip}")
        ip_data = json.loads(req_api.text)
        time.sleep(1)
        print(f"{Wh}\n IP target       :{Gr}", ip)
        print(f"{Wh} Type IP         :{Gr}", ip_data.get("type", "N/A"))
        print(f"{Wh} Country         :{Gr}", ip_data.get("country", "N/A"))
        print(f"{Wh} Country Code    :{Gr}", ip_data.get("country_code", "N/A"))
        print(f"{Wh} City            :{Gr}", ip_data.get("city", "N/A"))
        print(f"{Wh} Region          :{Gr}", ip_data.get("region", "N/A"))
        print(f"{Wh} Latitude        :{Gr}", ip_data.get("latitude", "N/A"))
        print(f"{Wh} Longitude       :{Gr}", ip_data.get("longitude", "N/A"))
        lat = ip_data.get('latitude', 0)
        lon = ip_data.get('longitude', 0)
        print(f"{Wh} Maps            :{Gr}", f"https://www.google.com/maps/@{lat},{lon},8z")
        print(f"{Wh} ISP             :{Gr}", ip_data.get("connection", {}).get("isp", "N/A"))
        print(f"{Wh} Organization    :{Gr}", ip_data.get("connection", {}).get("org", "N/A"))
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def showIP():
    try:
        respone = requests.get('https://api.ipify.org/')
        Show_IP = respone.text
        print(f"\n {Wh}========== {Gr}YOUR PUBLIC IP {Wh}==========")
        print(f"\n {Wh}[{Gr} + {Wh}] IP Address : {Gr}{Show_IP}")
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def phoneGW():
    User_phone = input(f"\n {Wh}Enter phone number (with country code, e.g., +6281xxxx) : {Gr}")
    try:
        parsed_number = phonenumbers.parse(User_phone, None)
        region_code = phonenumbers.region_code_for_number(parsed_number)
        provider = carrier.name_for_number(parsed_number, "en")
        location = geocoder.description_for_number(parsed_number, "id")
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)
        formatted_intl = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        timezones = timezone.time_zones_for_number(parsed_number)
        tz_str = ', '.join(timezones) if timezones else "N/A"

        print(f"\n {Wh}========== {Gr}PHONE NUMBER INFORMATION {Wh}==========")
        print(f"\n {Wh}Location         :{Gr} {location}")
        print(f" {Wh}Region Code      :{Gr} {region_code}")
        print(f" {Wh}Timezone         :{Gr} {tz_str}")
        print(f" {Wh}Operator         :{Gr} {provider if provider else 'Unknown'}")
        print(f" {Wh}Valid number     :{Gr} {is_valid}")
        print(f" {Wh}Possible number  :{Gr} {is_possible}")
        print(f" {Wh}International    :{Gr} {formatted_intl}")
        print(f" {Wh}Country code     :{Gr} +{parsed_number.country_code}")
        print(f" {Wh}Local number     :{Gr} {parsed_number.national_number}")
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def TrackLu():
    username = input(f"\n {Wh}Enter Username : {Gr}")
    results = {}
    social_media = [
        {"url": "https://www.facebook.com/{}", "name": "Facebook"},
        {"url": "https://www.twitter.com/{}", "name": "Twitter"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram"},
        {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
        {"url": "https://www.github.com/{}", "name": "GitHub"},
        {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
        {"url": "https://www.youtube.com/{}", "name": "YouTube"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
        {"url": "https://t.me/{}", "name": "Telegram"},
        {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
        {"url": "https://www.medium.com/@{}", "name": "Medium"},
    ]
    print(f"\n {Wh}========== {Gr}USERNAME SEARCH RESULTS {Wh}==========")
    for site in social_media:
        url = site['url'].format(username)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f" {Wh}[{Gr}+{Wh}] {site['name']}: {Gr}{url}")
            else:
                print(f" {Wh}[{Re}-{Wh}] {site['name']}: {Ye}Not found")
        except:
            print(f" {Wh}[{Re}-{Wh}] {site['name']}: {Ye}Error checking")

@is_option
def mac_lookup():
    mac = input(f"\n {Wh}Enter MAC Address (e.g., 00:11:22:AA:BB:CC) : {Gr}")
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}")
        if response.status_code == 200:
            vendor = response.text.strip()
            print(f"\n {Wh}========== {Gr}MAC ADDRESS VENDOR {Wh}==========")
            print(f" {Wh}MAC        : {Gr}{mac}")
            print(f" {Wh}Vendor     : {Gr}{vendor}")
        else:
            print(f"{Re} Vendor not found or invalid MAC.")
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def website_info():
    url = input(f"\n {Wh}Enter website URL (e.g., https://example.com) : {Gr}")
    if not url.startswith('http'):
        url = 'http://' + url
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        soup_text = response.text
        title_match = re.search(r'<title>(.*?)</title>', soup_text, re.IGNORECASE)
        title = title_match.group(1) if title_match else "No title found"
        server = response.headers.get('Server', 'Unknown')
        content_type = response.headers.get('Content-Type', 'Unknown')
        ip = socket.gethostbyname(urlparse(url).netloc)

        print(f"\n {Wh}========== {Gr}WEBSITE INFORMATION {Wh}==========")
        print(f" {Wh}URL         : {Gr}{url}")
        print(f" {Wh}IP Address  : {Gr}{ip}")
        print(f" {Wh}Server      : {Gr}{server}")
        print(f" {Wh}Content Type: {Gr}{content_type}")
        print(f" {Wh}Page Title  : {Gr}{title}")
        print(f" {Wh}Status Code : {Gr}{response.status_code}")
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def reverse_ip():
    ip = input(f"\n {Wh}Enter IP address for reverse lookup : {Gr}")
    try:
        response = requests.get(f"http://api.hackertarget.com/reverseiplookup/?q={ip}")
        if response.status_code == 200:
            domains = response.text.strip().split('\n')
            print(f"\n {Wh}========== {Gr}DOMAINS HOSTED ON IP {ip} {Wh}==========")
            for d in domains:
                if d and 'error' not in d.lower():
                    print(f" {Wh}[{Gr}+{Wh}] {Gr}{d}")
                else:
                    print(f" {Ye}No domains found or API limit reached.")
        else:
            print(f"{Re} API error.")
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def bin_lookup():
    bin_num = input(f"\n {Wh}Enter BIN (first 6 digits of credit card) : {Gr}")
    if not bin_num.isdigit() or len(bin_num) < 6:
        print(f"{Re} Please enter at least 6 digits.")
        return
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_num[:6]}")
        if response.status_code == 200:
            data = response.json()
            print(f"\n {Wh}========== {Gr}BIN INFORMATION {Wh}==========")
            print(f" {Wh}BIN        : {Gr}{bin_num[:6]}")
            print(f" {Wh}Scheme     : {Gr}{data.get('scheme', 'N/A')}")
            print(f" {Wh}Type       : {Gr}{data.get('type', 'N/A')}")
            print(f" {Wh}Brand      : {Gr}{data.get('brand', 'N/A')}")
            print(f" {Wh}Country    : {Gr}{data.get('country', {}).get('name', 'N/A')}")
            print(f" {Wh}Bank       : {Gr}{data.get('bank', {}).get('name', 'N/A')}")
        else:
            print(f"{Re} BIN not found or invalid.")
    except Exception as e:
        print(f"{Re} Error: {e}")

# ---------- MENU ----------
options = [
    {'num': 1, 'text': 'IP Tracker', 'func': IP_Track},
    {'num': 2, 'text': 'Show My IP', 'func': showIP},
    {'num': 3, 'text': 'Phone Number Tracker', 'func': phoneGW},
    {'num': 4, 'text': 'Username Tracker', 'func': TrackLu},
    {'num': 5, 'text': 'MAC Address Lookup', 'func': mac_lookup},
    {'num': 6, 'text': 'Website Info', 'func': website_info},
    {'num': 7, 'text': 'Reverse IP Lookup', 'func': reverse_ip},
    {'num': 8, 'text': 'BIN (Credit Card) Lookup', 'func': bin_lookup},
    {'num': 0, 'text': 'Exit', 'func': exit}
]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def call_option(opt):
    for option in options:
        if option['num'] == opt:
            if 'func' in option:
                option['func']()
                return
    raise ValueError('Option not found')

def execute_option(opt):
    try:
        call_option(opt)
        input(f'\n{Wh}[ {Gr}+ {Wh}] {Gr}Press Enter to continue...')
        main()
    except ValueError as e:
        print(e)
        time.sleep(2)
        execute_option(opt)
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exit')
        time.sleep(2)
        exit()

def option_text():
    text = ''
    for opt in options:
        text += f'{Wh}[ {opt["num"]} ] {Gr}{opt["text"]}\n'
    return text

def option():
    clear()
    stderr.writelines(f"""
{Wh}╔════════════════════════════════════════════════════╗
{Wh}║      {Gr}██████╗  █████╗ ██████╗ ██╗  ██╗             {Wh}║
{Wh}║      {Gr}██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝             {Wh}║
{Wh}║      {Gr}██║  ██║███████║██████╔╝█████╔╝              {Wh}║
{Wh}║      {Gr}██║  ██║██╔══██║██╔══██╗██╔═██╗              {Wh}║
{Wh}║      {Gr}██████╔╝██║  ██║██║  ██║██║  ██╗             {Wh}║
{Wh}║      {Gr}╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝             {Wh}║
{Wh}║                 {Cy}ADVANCED TRACKER                  {Wh}║
{Wh}╚════════════════════════════════════════════════════╝
    """)
    stderr.writelines(f"\n\n{option_text()}")

def run_banner():
    clear()
    time.sleep(1)
    stderr.writelines(f"""{Wh}
╔════════════════════════════════════════════════════╗
║                 {Gr}DARKX TRACKER                    {Wh}║
║             {Cy}-----------------------              {Wh}║
║         {Wh}[ {Gr}IP • PHONE • USERNAME • MAC {Wh}]        ║
║         {Wh}[ {Gr}WEBSITE • REVERSE IP • BIN {Wh}]        ║
║                                                    ║
║        {Mage}Let the hunt begin...                    {Wh}║
╚════════════════════════════════════════════════════╝
    """)
    time.sleep(0.5)

def main():
    clear()
    option()
    time.sleep(1)
    try:
        opt = int(input(f"{Wh}\n [ + ] {Gr}Select Option : {Wh}"))
        execute_option(opt)
    except ValueError:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Please input a number')
        time.sleep(2)
        main()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exit')
        time.sleep(2)
        exit()
