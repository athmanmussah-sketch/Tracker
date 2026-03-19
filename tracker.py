#!/usr/bin/python
# DARKX TOOL - ADVANCED TRACKER PRO
# “Wahai orang-orang yang beriman! Janganlah kamu saling memakan harta sesamamu dengan jalan yang batil,” (QS. An Nisaa': 29). 
# Rasulullah SAW juga melarang umatnya untuk mengambil hak orang lain tanpa izin.

import json
import requests
import time
import os
import phonenumbers
import re
import socket
import dns.resolver
import whois
import hashlib
import base64
import subprocess
import sys
from phonenumbers import carrier, geocoder, timezone
from sys import stderr
from urllib.parse import urlparse
from datetime import datetime
import shodan
import folium
import webbrowser
from bs4 import BeautifulSoup
import pandas as pd
from colorama import init, Fore, Back, Style
import scapy.all as scapy
import netifaces
import paramiko
import sqlite3
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import nmap
import geoip2.database
import pygeoip
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# Colors
Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'

# Database setup
def setup_database():
    conn = sqlite3.connect('darkx_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ip_history
                     (id INTEGER PRIMARY KEY, ip TEXT, data TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS phone_history
                     (id INTEGER PRIMARY KEY, phone TEXT, data TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS username_history
                     (id INTEGER PRIMARY KEY, username TEXT, data TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

setup_database()

def save_to_db(table, key, data):
    conn = sqlite3.connect('darkx_tracker.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table} ({table.split('_')[0]}, data) VALUES (?, ?)", (key, json.dumps(data)))
    conn.commit()
    conn.close()

def load_from_db(table, key):
    conn = sqlite3.connect('darkx_tracker.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT data FROM {table} WHERE {table.split('_')[0]} = ? ORDER BY timestamp DESC LIMIT 1", (key,))
    result = cursor.fetchone()
    conn.close()
    return json.loads(result[0]) if result else None

# utilities
def is_option(func):
    def wrapper(*args, **kwargs):
        run_banner()
        func(*args, **kwargs)
    return wrapper

# ---------- TRACKING FUNCTIONS ----------

@is_option
def IP_Track_Advanced():
    ip = input(f"{Wh}\n Enter IP target : {Gr}")
    print()
    print(f' {Wh}╔════════════════════════════════════════════════════╗')
    print(f' {Wh}║         {Gr}ADVANCED IP ADDRESS INFORMATION         {Wh}║')
    print(f' {Wh}╚════════════════════════════════════════════════════╝')
    
    try:
        # Multiple API calls for comprehensive data
        # API 1: ipwho.is
        req_api = requests.get(f"http://ipwho.is/{ip}")
        ip_data = json.loads(req_api.text)
        
        # API 2: ip-api.com
        req_api2 = requests.get(f"http://ip-api.com/json/{ip}")
        ip_data2 = json.loads(req_api2.text)
        
        # API 3: ipinfo.io
        req_api3 = requests.get(f"https://ipinfo.io/{ip}/json")
        ip_data3 = json.loads(req_api3.text)
        
        # DNS Lookup
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = "N/A"
        
        # Port Scanning (common ports)
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        open_ports = []
        for port in common_ports[:10]:  # Check first 10 to avoid long delay
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        
        time.sleep(1)
        print(f"{Wh}\n┌─[ BASIC INFORMATION ]")
        print(f"{Wh}├─ IP target       :{Gr} {ip}")
        print(f"{Wh}├─ Hostname        :{Gr} {hostname}")
        print(f"{Wh}├─ Type IP         :{Gr} {ip_data.get('type', 'N/A')}")
        print(f"{Wh}├─ Country         :{Gr} {ip_data.get('country', 'N/A')}")
        print(f"{Wh}├─ Country Code    :{Gr} {ip_data.get('country_code', 'N/A')}")
        print(f"{Wh}├─ Region          :{Gr} {ip_data.get('region', 'N/A')}")
        print(f"{Wh}├─ City            :{Gr} {ip_data.get('city', 'N/A')}")
        print(f"{Wh}├─ Latitude        :{Gr} {ip_data.get('latitude', 'N/A')}")
        print(f"{Wh}├─ Longitude       :{Gr} {ip_data.get('longitude', 'N/A')}")
        
        lat = ip_data.get('latitude', 0)
        lon = ip_data.get('longitude', 0)
        print(f"{Wh}├─ Maps            :{Gr} https://www.google.com/maps/@{lat},{lon},12z")
        print(f"{Wh}├─ Timezone        :{Gr} {ip_data.get('timezone', {}).get('id', 'N/A')}")
        
        print(f"{Wh}\n┌─[ NETWORK INFORMATION ]")
        print(f"{Wh}├─ ISP             :{Gr} {ip_data.get('connection', {}).get('isp', 'N/A')}")
        print(f"{Wh}├─ Organization    :{Gr} {ip_data.get('connection', {}).get('org', 'N/A')}")
        print(f"{Wh}├─ ASN             :{Gr} {ip_data.get('connection', {}).get('asn', 'N/A')}")
        print(f"{Wh}├─ Open Ports      :{Gr} {', '.join(map(str, open_ports)) if open_ports else 'None found'}")
        
        print(f"{Wh}\n┌─[ GEOLOCATION DETAILS ]")
        print(f"{Wh}├─ ZIP Code        :{Gr} {ip_data2.get('zip', 'N/A')}")
        print(f"{Wh}├─ Timezone (alt)  :{Gr} {ip_data2.get('timezone', 'N/A')}")
        print(f"{Wh}├─ Organization    :{Gr} {ip_data3.get('org', 'N/A')}")
        
        # Save to database
        save_to_db('ip_history', ip, ip_data)
        
        # Option to view previous history
        prev_data = load_from_db('ip_history', ip)
        if prev_data:
            print(f"{Wh}\n┌─[ PREVIOUS SEARCHES ]")
            print(f"{Wh}├─ Previous data found for this IP")
        
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def IP_Range_Scan():
    network = input(f"{Wh}\n Enter network range (e.g., 192.168.1.0/24) : {Gr}")
    print(f"{Wh}\n Scanning network... This may take a while")
    
    try:
        # Create ARP request
        arp_request = scapy.ARP(pdst=network)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        
        # Send packet and receive response
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
        
        devices = []
        for element in answered_list:
            device = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            devices.append(device)
        
        print(f"{Wh}\n╔════════════════════════════════════════════════════╗")
        print(f"{Wh}║         {Gr}ACTIVE DEVICES IN NETWORK                {Wh}║")
        print(f"{Wh}╚════════════════════════════════════════════════════╝")
        print(f"{Wh}\n{'IP Address':<20} {'MAC Address':<20}")
        print(f"{Wh}{'─'*40}")
        for device in devices:
            print(f"{Gr}{device['ip']:<20} {device['mac']:<20}")
        
        print(f"{Wh}\n Total devices found: {len(devices)}")
        
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def Phone_Track_Advanced():
    User_phone = input(f"\n {Wh}Enter phone number (with country code, e.g., +6281xxxx) : {Gr}")
    try:
        parsed_number = phonenumbers.parse(User_phone, None)
        region_code = phonenumbers.region_code_for_number(parsed_number)
        provider = carrier.name_for_number(parsed_number, "en")
        location = geocoder.description_for_number(parsed_number, "id")
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)
        formatted_intl = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        formatted_national = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        formatted_e164 = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        timezones = timezone.time_zones_for_number(parsed_number)
        tz_str = ', '.join(timezones) if timezones else "N/A"
        
        # Get number type
        number_type = phonenumbers.number_type(parsed_number)
        type_map = {
            0: "FIXED_LINE",
            1: "MOBILE",
            2: "FIXED_LINE_OR_MOBILE", 
            3: "TOLL_FREE",
            4: "PREMIUM_RATE",
            5: "SHARED_COST",
            6: "VOIP",
            7: "PERSONAL_NUMBER",
            8: "PAGER",
            9: "UAN",
            10: "VOICEMAIL"
        }
        number_type_str = type_map.get(number_type, "UNKNOWN")
        
        # Try to get additional info from online APIs
        additional_info = {}
        try:
            # Numverify API (limited, but worth trying)
            access_key = "YOUR_API_KEY"  # User would need to add their own
            # response = requests.get(f"http://apilayer.net/api/validate?access_key={access_key}&number={User_phone}")
            # if response.status_code == 200:
            #     additional_info = response.json()
            pass
        except:
            pass
        
        print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
        print(f" {Wh}║         {Gr}ADVANCED PHONE NUMBER INFORMATION        {Wh}║")
        print(f" {Wh}╚════════════════════════════════════════════════════╝")
        
        print(f"{Wh}\n┌─[ BASIC INFORMATION ]")
        print(f"{Wh}├─ Number           :{Gr} {User_phone}")
        print(f"{Wh}├─ International    :{Gr} {formatted_intl}")
        print(f"{Wh}├─ National         :{Gr} {formatted_national}")
        print(f"{Wh}├─ E.164 Format     :{Gr} {formatted_e164}")
        print(f"{Wh}├─ Country Code     :{Gr} +{parsed_number.country_code}")
        print(f"{Wh}├─ Local Number     :{Gr} {parsed_number.national_number}")
        
        print(f"{Wh}\n┌─[ LOCATION INFORMATION ]")
        print(f"{Wh}├─ Location         :{Gr} {location if location else 'Unknown'}")
        print(f"{Wh}├─ Region Code      :{Gr} {region_code}")
        print(f"{Wh}├─ Timezone         :{Gr} {tz_str}")
        
        print(f"{Wh}\n┌─[ NETWORK INFORMATION ]")
        print(f"{Wh}├─ Carrier/Provider :{Gr} {provider if provider else 'Unknown'}")
        print(f"{Wh}├─ Number Type      :{Gr} {number_type_str}")
        
        print(f"{Wh}\n┌─[ VALIDATION ]")
        print(f"{Wh}├─ Valid number     :{Gr} {is_valid}")
        print(f"{Wh}├─ Possible number  :{Gr} {is_possible}")
        
        # Generate possible carrier variations
        if provider:
            print(f"{Wh}\n┌─[ POSSIBLE CARRIER INFO ]")
            print(f"{Wh}├─ Primary Carrier :{Gr} {provider}")
        
        # Save to database
        save_to_db('phone_history', User_phone, {
            'number': User_phone,
            'location': location,
            'provider': provider,
            'valid': is_valid
        })
        
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def Username_Track_Advanced():
    username = input(f"\n {Wh}Enter Username : {Gr}")
    results = {}
    
    # Extended social media list
    social_media = [
        {"url": "https://www.facebook.com/{}", "name": "Facebook", "category": "Social"},
        {"url": "https://www.twitter.com/{}", "name": "Twitter/X", "category": "Social"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram", "category": "Social"},
        {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn", "category": "Professional"},
        {"url": "https://www.github.com/{}", "name": "GitHub", "category": "Development"},
        {"url": "https://www.pinterest.com/{}", "name": "Pinterest", "category": "Social"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok", "category": "Social"},
        {"url": "https://www.youtube.com/{}", "name": "YouTube", "category": "Video"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat", "category": "Social"},
        {"url": "https://t.me/{}", "name": "Telegram", "category": "Messaging"},
        {"url": "https://www.twitch.tv/{}", "name": "Twitch", "category": "Gaming"},
        {"url": "https://www.medium.com/@{}", "name": "Medium", "category": "Blogging"},
        {"url": "https://www.reddit.com/user/{}", "name": "Reddit", "category": "Social"},
        {"url": "https://www.tumblr.com/blog/{}", "name": "Tumblr", "category": "Blogging"},
        {"url": "https://www.flickr.com/people/{}", "name": "Flickr", "category": "Photo"},
        {"url": "https://www.behance.net/{}", "name": "Behance", "category": "Portfolio"},
        {"url": "https://dribbble.com/{}", "name": "Dribbble", "category": "Design"},
        {"url": "https://www.soundcloud.com/{}", "name": "SoundCloud", "category": "Music"},
        {"url": "https://www.mixcloud.com/{}", "name": "MixCloud", "category": "Music"},
        {"url": "https://www.spotify.com/user/{}", "name": "Spotify", "category": "Music"},
        {"url": "https://www.patreon.com/{}", "name": "Patreon", "category": "Funding"},
        {"url": "https://www.producthunt.com/@{}", "name": "ProductHunt", "category": "Tech"},
        {"url": "https://keybase.io/{}", "name": "Keybase", "category": "Security"},
        {"url": "https://www.wattpad.com/user/{}", "name": "Wattpad", "category": "Writing"},
        {"url": "https://archive.org/details/@{}", "name": "Archive.org", "category": "Archive"},
        {"url": "https://www.quora.com/profile/{}", "name": "Quora", "category": "Q&A"},
        {"url": "https://stackoverflow.com/users/{}", "name": "StackOverflow", "category": "Development"},
        {"url": "https://news.ycombinator.com/user?id={}", "name": "HackerNews", "category": "Tech"},
        {"url": "https://en.gravatar.com/{}", "name": "Gravatar", "category": "Avatar"},
        {"url": "https://about.me/{}", "name": "About.me", "category": "Bio"},
        {"url": "https://angel.co/u/{}", "name": "AngelList", "category": "Startup"},
        {"url": "https://www.crunchbase.com/person/{}", "name": "CrunchBase", "category": "Business"},
        {"url": "https://www.kickstarter.com/profile/{}", "name": "Kickstarter", "category": "Funding"},
        {"url": "https://www.indiegogo.com/individuals/{}", "name": "IndieGoGo", "category": "Funding"},
        {"url": "https://www.fiverr.com/{}", "name": "Fiverr", "category": "Freelance"},
        {"url": "https://www.upwork.com/fl/{}", "name": "Upwork", "category": "Freelance"},
        {"url": "https://www.freelancer.com/u/{}", "name": "Freelancer", "category": "Freelance"},
        {"url": "https://www.etsy.com/people/{}", "name": "Etsy", "category": "Marketplace"},
        {"url": "https://www.roblox.com/user.aspx?username={}", "name": "Roblox", "category": "Gaming"},
        {"url": "https://steamcommunity.com/id/{}", "name": "Steam", "category": "Gaming"},
        {"url": "https://www.chess.com/member/{}", "name": "Chess.com", "category": "Gaming"},
        {"url": "https://lichess.org/@/{}", "name": "Lichess", "category": "Gaming"},
        {"url": "https://www.codecademy.com/profiles/{}", "name": "Codecademy", "category": "Learning"},
        {"url": "https://www.coursera.org/user/{}", "name": "Coursera", "category": "Learning"},
        {"url": "https://www.udemy.com/user/{}", "name": "Udemy", "category": "Learning"},
        {"url": "https://www.khanacademy.org/profile/{}", "name": "KhanAcademy", "category": "Learning"},
        {"url": "https://www.duolingo.com/profile/{}", "name": "Duolingo", "category": "Learning"},
        {"url": "https://www.goodreads.com/{}", "name": "Goodreads", "category": "Books"},
        {"url": "https://www.imdb.com/user/ur{}/", "name": "IMDb", "category": "Movies"},
        {"url": "https://letterboxd.com/{}", "name": "Letterboxd", "category": "Movies"},
        {"url": "https://www.last.fm/user/{}", "name": "Last.fm", "category": "Music"},
        {"url": "https://www.deviantart.com/{}", "name": "DeviantArt", "category": "Art"},
        {"url": "https://www.artstation.com/{}", "name": "ArtStation", "category": "Art"},
        {"url": "https://unsplash.com/@{}", "name": "Unsplash", "category": "Photo"},
        {"url": "https://500px.com/p/{}", "name": "500px", "category": "Photo"},
        {"url": "https://www.strava.com/athletes/{}", "name": "Strava", "category": "Sports"},
        {"url": "https://www.fitbit.com/user/{}", "name": "Fitbit", "category": "Health"},
        {"url": "https://www.myfitnesspal.com/profile/{}", "name": "MyFitnessPal", "category": "Health"},
    ]
    
    print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
    print(f" {Wh}║         {Gr}ADVANCED USERNAME SEARCH RESULTS         {Wh}║")
    print(f" {Wh}╚════════════════════════════════════════════════════╝")
    
    found_count = 0
    categories_found = set()
    
    for site in social_media:
        url = site['url'].format(username)
        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                print(f" {Wh}[{Gr}✓{Wh}] {site['category']:<12} : {Gr}{site['name']:<15} {Wh}-> {Cy}{url}")
                found_count += 1
                categories_found.add(site['category'])
            else:
                print(f" {Wh}[{Re}✗{Wh}] {site['category']:<12} : {Gr}{site['name']:<15} {Wh}-> {Ye}Not found")
        except:
            print(f" {Wh}[{Re}✗{Wh}] {site['category']:<12} : {Gr}{site['name']:<15} {Wh}-> {Re}Error checking")
    
    print(f"\n {Wh}┌─[ SUMMARY ]")
    print(f" {Wh}├─ Total profiles found : {Gr}{found_count}")
    print(f" {Wh}├─ Categories found     : {Gr}{', '.join(categories_found) if categories_found else 'None'}")
    print(f" {Wh}└─ Search complete for   : {Gr}{username}")
    
    # Save to database
    save_to_db('username_history', username, {
        'username': username,
        'found': found_count,
        'categories': list(categories_found)
    })

@is_option
def Website_Analyzer():
    url = input(f"\n {Wh}Enter website URL (e.g., https://example.com) : {Gr}")
    if not url.startswith('http'):
        url = 'http://' + url
    
    try:
        print(f"{Wh}\n Analyzing website... This may take a moment")
        
        # Basic request
        response = requests.get(url, timeout=10, allow_redirects=True, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get IP
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)
        
        # WHOIS info
        try:
            whois_info = whois.whois(domain)
        except:
            whois_info = None
        
        # DNS records
        dns_records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        for record in record_types:
            try:
                answers = dns.resolver.resolve(domain, record)
                dns_records[record] = [str(r) for r in answers]
            except:
                dns_records[record] = []
        
        # Headers analysis
        headers = response.headers
        
        # Security headers check
        security_headers = {
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy': 'CSP',
            'X-Frame-Options': 'Clickjacking Protection',
            'X-Content-Type-Options': 'MIME Sniffing Prevention',
            'X-XSS-Protection': 'XSS Protection',
            'Referrer-Policy': 'Referrer Policy',
            'Permissions-Policy': 'Permissions Policy'
        }
        
        print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
        print(f" {Wh}║         {Gr}ADVANCED WEBSITE ANALYSIS              {Wh}║")
        print(f" {Wh}╚════════════════════════════════════════════════════╝")
        
        print(f"{Wh}\n┌─[ BASIC INFORMATION ]")
        print(f"{Wh}├─ URL            : {Gr}{url}")
        print(f"{Wh}├─ Domain         : {Gr}{domain}")
        print(f"{Wh}├─ IP Address     : {Gr}{ip}")
        print(f"{Wh}├─ Server         : {Gr}{headers.get('Server', 'Unknown')}")
        print(f"{Wh}├─ Technology     : {Gr}{headers.get('X-Powered-By', 'Unknown')}")
        print(f"{Wh}├─ Status Code    : {Gr}{response.status_code}")
        print(f"{Wh}├─ Response Time  : {Gr}{response.elapsed.total_seconds():.2f}s")
        
        print(f"{Wh}\n┌─[ PAGE INFORMATION ]")
        print(f"{Wh}├─ Title          : {Gr}{soup.title.string if soup.title else 'No title'}")
        print(f"{Wh}├─ Meta Description : {Gr}{soup.find('meta', attrs={'name':'description'}).get('content', 'N/A') if soup.find('meta', attrs={'name':'description'}) else 'N/A'}")
        print(f"{Wh}├─ Meta Keywords  : {Gr}{soup.find('meta', attrs={'name':'keywords'}).get('content', 'N/A') if soup.find('meta', attrs={'name':'keywords'}) else 'N/A'}")
        print(f"{Wh}├─ Content Type   : {Gr}{headers.get('Content-Type', 'Unknown')}")
        print(f"{Wh}├─ Content Length : {Gr}{headers.get('Content-Length', 'Unknown')} bytes")
        
        print(f"{Wh}\n┌─[ SECURITY ANALYSIS ]")
        for header, description in security_headers.items():
            status = headers.get(header, 'Not Found')
            if status != 'Not Found':
                print(f"{Wh}├─ {description:<25} : {Gr}✓ Present")
            else:
                print(f"{Wh}├─ {description:<25} : {Re}✗ Missing")
        
        print(f"{Wh}\n┌─[ DNS RECORDS ]")
        for record_type, records in dns_records.items():
            if records:
                print(f"{Wh}├─ {record_type} Records   : {Gr}{', '.join(records[:3])}")
                if len(records) > 3:
                    print(f"{Wh}│                        {Gr}... and {len(records)-3} more")
        
        print(f"{Wh}\n┌─[ WHOIS INFORMATION ]")
        if whois_info:
            if whois_info.registrar:
                print(f"{Wh}├─ Registrar      : {Gr}{whois_info.registrar}")
            if whois_info.creation_date:
                creation = whois_info.creation_date[0] if isinstance(whois_info.creation_date, list) else whois_info.creation_date
                print(f"{Wh}├─ Created        : {Gr}{creation}")
            if whois_info.expiration_date:
                expiration = whois_info.expiration_date[0] if isinstance(whois_info.expiration_date, list) else whois_info.expiration_date
                print(f"{Wh}├─ Expires        : {Gr}{expiration}")
            if whois_info.name_servers:
                print(f"{Wh}├─ Name Servers   : {Gr}{', '.join(whois_info.name_servers[:3])}")
        
        # Email extraction
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
        if emails:
            print(f"{Wh}\n┌─[ EMAILS FOUND ]")
            for email in set(emails[:5]):  # Show first 5 unique emails
                print(f"{Wh}├─ {Gr}{email}")
        
        # Links analysis
        links = soup.find_all('a', href=True)
        external_links = []
        internal_links = []
        for link in links:
            href = link['href']
            if href.startswith('http'):
                if domain in href:
                    internal_links.append(href)
                else:
                    external_links.append(href)
        
        print(f"{Wh}\n┌─[ LINKS ANALYSIS ]")
        print(f"{Wh}├─ Total Links    : {Gr}{len(links)}")
        print(f"{Wh}├─ Internal Links : {Gr}{len(internal_links)}")
        print(f"{Wh}├─ External Links : {Gr}{len(external_links)}")
        
        # Forms detection
        forms = soup.find_all('form')
        if forms:
            print(f"{Wh}\n┌─[ FORMS DETECTED ]")
            print(f"{Wh}├─ Total Forms    : {Gr}{len(forms)}")
            for i, form in enumerate(forms[:3]):  # Show first 3 forms
                method = form.get('method', 'GET').upper()
                action = form.get('action', 'N/A')
                print(f"{Wh}├─ Form {i+1}         : {Gr}{method} -> {action}")
        
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def Email_Tracker():
    email = input(f"\n {Wh}Enter email address : {Gr}")
    
    try:
        print(f"{Wh}\n Analyzing email...")
        
        # Extract domain
        domain = email.split('@')[1] if '@' in email else None
        
        print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
        print(f" {Wh}║         {Gr}EMAIL ADDRESS ANALYSIS                   {Wh}║")
        print(f" {Wh}╚════════════════════════════════════════════════════╝")
        
        print(f"{Wh}\n┌─[ BASIC INFORMATION ]")
        print(f"{Wh}├─ Email          : {Gr}{email}")
        print(f"{Wh}├─ Domain         : {Gr}{domain if domain else 'Invalid'}")
        
        if domain:
            # Check if email domain exists
            try:
                ip = socket.gethostbyname(domain)
                print(f"{Wh}├─ Domain IP      : {Gr}{ip}")
            except:
                print(f"{Wh}├─ Domain IP      : {Re}Could not resolve")
            
            # MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                print(f"{Wh}├─ MX Records     : {Gr}{len(mx_records)} found")
                for mx in mx_records[:3]:
                    print(f"{Wh}│                  {Gr}{mx.exchange} (priority {mx.preference})")
            except:
                print(f"{Wh}├─ MX Records     : {Re}None found")
        
        # Check if email is from common providers
        common_providers = {
            'gmail.com': 'Google Mail',
            'yahoo.com': 'Yahoo Mail',
            'hotmail.com': 'Microsoft Outlook',
            'outlook.com': 'Microsoft Outlook',
            'aol.com': 'AOL Mail',
            'protonmail.com': 'ProtonMail',
            'mail.com': 'Mail.com',
            'yandex.com': 'Yandex Mail',
            'gmx.com': 'GMX Mail',
            'icloud.com': 'Apple iCloud'
        }
        
        provider = common_providers.get(domain, 'Custom/Private Domain')
        print(f"{Wh}├─ Provider       : {Gr}{provider}")
        
        # Check email format validity
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid_format = re.match(email_regex, email) is not None
        print(f"{Wh}├─ Valid Format   : {Gr}{is_valid_format}")
        
        # Generate possible social media links
        username = email.split('@')[0]
        print(f"{Wh}\n┌─[ POSSIBLE SOCIAL MEDIA ]")
        print(f"{Wh}├─ Try searching username: {Gr}{username}")
        print(f"{Wh}├─ Facebook   : {Gr}https://www.facebook.com/search/top?q={username}")
        print(f"{Wh}├─ Twitter    : {Gr}https://twitter.com/search?q={username}")
        print(f"{Wh}├─ Instagram  : {Gr}https://www.instagram.com/{username}/")
        print(f"{Wh}├─ LinkedIn   : {Gr}https://www.linkedin.com/search/results/all/?keywords={username}")
        print(f"{Wh}├─ GitHub     : {Gr}https://github.com/search?q={username}")
        
        # Check for Gravatar
        email_hash = hashlib.md5(email.lower().encode()).hexdigest()
        gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        try:
            gravatar_response = requests.get(gravatar_url)
            if gravatar_response.status_code == 200:
                print(f"{Wh}├─ Gravatar    : {Gr}Profile exists")
                print(f"{Wh}│              {Cy}{gravatar_url}")
            else:
                print(f"{Wh}├─ Gravatar    : {Ye}No profile found")
        except:
            print(f"{Wh}├─ Gravatar    : {Re}Could not check")
        
        # Check for data breaches (using haveibeenpwned API - note: requires API key)
        print(f"{Wh}\n┌─[ BREACH CHECK ]")
        print(f"{Wh}├─ Check if email was in breaches: {Cy}https://haveibeenpwned.com/account/{email}")
        
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def Port_Scanner():
    target = input(f"\n {Wh}Enter target IP or domain : {Gr}")
    port_range = input(f"{Wh}Enter port range (e.g., 1-1000) or press Enter for common ports : {Gr}")
    
    try:
        # Resolve domain to IP if needed
        try:
            ip = socket.gethostbyname(target)
        except:
            ip = target
        
        if port_range:
            start_port, end_port = map(int, port_range.split('-'))
            ports = range(start_port, end_port + 1)
        else:
            # Common ports
            ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443, 8888]
        
        print(f"{Wh}\n Scanning {ip}... This may take a while")
        print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
        print(f" {Wh}║         {Gr}PORT SCAN RESULTS                        {Wh}║")
        print(f" {Wh}╚════════════════════════════════════════════════════╝")
        print(f"{Wh}\n{'PORT':<10} {'STATE':<10} {'SERVICE':<15}")
        print(f"{Wh}{'─'*35}")
        
        open_ports = []
        service_map = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS', 
            80: 'HTTP', 110: 'POP3', 111: 'RPC', 135: 'RPC', 139: 'NetBIOS',
            143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 993: 'IMAPS', 995: 'POP3S',
            1723: 'PPTP', 3306: 'MySQL', 3389: 'RDP', 5900: 'VNC', 8080: 'HTTP-Alt',
            8443: 'HTTPS-Alt', 8888: 'HTTP-Alt'
        }
        
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                service = service_map.get(port, 'Unknown')
                print(f"{Gr}{port:<10} open       {service:<15}")
                open_ports.append(port)
            sock.close()
        
        if not open_ports:
            print(f"{Ye} No open ports found")
        
        print(f"\n{Wh} Total open ports: {len(open_ports)}")
        
        # Banner grabbing on open ports
        if open_ports:
            print(f"{Wh}\n┌─[ BANNER GRABBING ]")
            for port in open_ports[:5]:  # Limit to first 5 to avoid long delay
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((ip, port))
                    sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                    banner = sock.recv(1024).decode().strip()
                    print(f"{Wh}├─ Port {port:<5}: {Gr}{banner[:50]}...")
                    sock.close()
                except:
                    pass
        
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def Hash_Cracker():
    print(f"{Wh}\n Available hash types:")
    print(f"{Wh} 1. MD5")
    print(f"{Wh} 2. SHA1")
    print(f"{Wh} 3. SHA256")
    print(f"{Wh} 4. SHA512")
    
    hash_type = input(f"\n{Wh} Select hash type (1-4) : {Gr}")
    hash_value = input(f"{Wh} Enter hash value : {Gr}")
    
    hash_types = {
        '1': hashlib.md5,
        '2': hashlib.sha1,
        '3': hashlib.sha256,
        '4': hashlib.sha512
    }
    
    if hash_type not in hash_types:
        print(f"{Re} Invalid hash type")
        return
    
    print(f"{Wh}\n Attempting to crack hash...")
    
    # Common wordlist (simplified for demo)
    wordlist = ['password', '123456', 'admin', 'root', 'qwerty', 'abc123', 'letmein', 'welcome', 'monkey', 'dragon']
    
    found = False
    for word in wordlist:
        test_hash = hash_types[hash_type](word.encode()).hexdigest()
        if test_hash == hash_value:
            print(f"{Gr}\n[+] Hash cracked!")
            print(f"{Wh} Original text: {Gr}{word}")
            found = True
            break
    
    if not found:
        print(f"{Re} Hash not found in wordlist")

@is_option
def Metadata_Extractor():
    file_path = input(f"\n {Wh}Enter file path (image/document) : {Gr}")
    
    if not os.path.exists(file_path):
        print(f"{Re} File not found")
        return
    
    print(f"{Wh}\n Extracting metadata...")
    
    try:
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # For images, we could use PIL/Pillow
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            image = Image.open(file_path)
            print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
            print(f" {Wh}║         {Gr}IMAGE METADATA                            {Wh}║")
            print(f" {Wh}╚════════════════════════════════════════════════════╝")
            
            print(f"{Wh}\n┌─[ BASIC INFO ]")
            print(f"{Wh}├─ Format        : {Gr}{image.format}")
            print(f"{Wh}├─ Size          : {Gr}{image.size}")
            print(f"{Wh}├─ Mode          : {Gr}{image.mode}")
            
            # EXIF data
            exifdata = image.getexif()
            if exifdata:
                print(f"{Wh}\n┌─[ EXIF DATA ]")
                for tag_id, value in exifdata.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if isinstance(value, bytes):
                        value = value.decode(errors='ignore')
                    print(f"{Wh}├─ {tag:<20}: {Gr}{value}")
            else:
                print(f"{Wh}\n┌─[ EXIF DATA ]")
                print(f"{Wh}├─ No EXIF data found")
        
        elif file_path.lower().endswith(('.pdf')):
            # For PDFs, we could use PyPDF2
            import PyPDF2
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                info = pdf_reader.metadata
                
                print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
                print(f" {Wh}║         {Gr}PDF METADATA                             {Wh}║")
                print(f" {Wh}╚════════════════════════════════════════════════════╝")
                
                if info:
                    for key, value in info.items():
                        print(f"{Wh}├─ {key.replace('/', '')}: {Gr}{value}")
                else:
                    print(f"{Wh}├─ No metadata found")
        
        elif file_path.lower().endswith(('.docx', '.xlsx', '.pptx')):
            # For Office documents
            import zipfile
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                if 'docProps/core.xml' in zip_file.namelist():
                    with zip_file.open('docProps/core.xml') as core_file:
                        content = core_file.read().decode()
                        # Simple extraction, would need proper XML parsing
                        print(f"{Wh}\n Metadata found in document")
        
        else:
            # Generic file info
            file_stat = os.stat(file_path)
            print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
            print(f" {Wh}║         {Gr}FILE INFORMATION                          {Wh}║")
            print(f" {Wh}╚════════════════════════════════════════════════════╝")
            print(f"{Wh}\n├─ File size     : {Gr}{file_stat.st_size} bytes")
            print(f"{Wh}├─ Created       : {Gr}{datetime.fromtimestamp(file_stat.st_ctime)}")
            print(f"{Wh}├─ Modified      : {Gr}{datetime.fromtimestamp(file_stat.st_mtime)}")
            print(f"{Wh}├─ Accessed      : {Gr}{datetime.fromtimestamp(file_stat.st_atime)}")
            
    except Exception as e:
        print(f"{Re} Error extracting metadata: {e}")

@is_option
def DNS_Enumeration():
    domain = input(f"\n {Wh}Enter domain : {Gr}")
    
    try:
        print(f"{Wh}\n Enumerating DNS records for {domain}...")
        
        record_types = {
            'A': 'IPv4 Address',
            'AAAA': 'IPv6 Address',
            'MX': 'Mail Exchange',
            'NS': 'Name Server',
            'TXT': 'Text Record',
            'SOA': 'Start of Authority',
            'CNAME': 'Canonical Name',
            'PTR': 'Pointer',
            'SRV': 'Service'
        }
        
        print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
        print(f" {Wh}║         {Gr}DNS ENUMERATION RESULTS                   {Wh}║")
        print(f" {Wh}╚════════════════════════════════════════════════════╝")
        
        for record_type, description in record_types.items():
            try:
                answers = dns.resolver.resolve(domain, record_type)
                print(f"{Wh}\n┌─[ {description} ({record_type}) ]")
                for i, answer in enumerate(answers[:5], 1):
                    print(f"{Wh}├─ {Gr}{answer}")
                if len(answers) > 5:
                    print(f"{Wh}│  {Gr}... and {len(answers)-5} more")
            except dns.resolver.NoAnswer:
                continue
            except dns.resolver.NXDOMAIN:
                print(f"{Re} Domain does not exist")
                break
            except Exception as e:
                continue
        
        # Zone transfer attempt
        print(f"{Wh}\n┌─[ ZONE TRANSFER ATTEMPT ]")
        try:
            ns_records = dns.resolver.resolve(domain, 'NS')
            for ns in ns_records:
                ns_domain = str(ns).rstrip('.')
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(ns_domain, domain))
                    if zone:
                        print(f"{Wh}├─ {Gr}Zone transfer successful from {ns_domain}")
                        for name, node in zone.nodes.items():
                            print(f"{Wh}│  {Gr}{name}")
                except:
                    print(f"{Wh}├─ {Re}Zone transfer failed from {ns_domain}")
        except:
            print(f"{Wh}├─ {Re}Could not attempt zone transfer")
        
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def Subdomain_Finder():
    domain = input(f"\n {Wh}Enter domain : {Gr}")
    
    # Common subdomains wordlist
    subdomains = [
        'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
        'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test',
        'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3',
        'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 'static',
        'docs', 'resources', 'intranet', 'portal', 'demo', 'info', 'cs', 'email',
        'images', 'img', 'www1', 'help', 'secure', 'apps', 'kb', 'store', 'beta',
        'status', 'dns', 'web', 'api', 'app', 'stage', 'staging', 'test2', 'test1',
        'chat', 'video', 'media', 'cloud', 'files', 'archive', 'backup', 'dev2',
        'download', 'downloads', 'upload', 'uploads', 'server', 'db', 'database',
        'sql', 'data', 'stats', 'stat', 'analytics', 'report', 'reports', 'log'
    ]
    
    found_subdomains = []
    
    print(f"{Wh}\n Searching for subdomains of {domain}...")
    print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
    print(f" {Wh}║         {Gr}SUBDOMAIN FINDER RESULTS                  {Wh}║")
    print(f" {Wh}╚════════════════════════════════════════════════════╝")
    
    for subdomain in subdomains:
        full_domain = f"{subdomain}.{domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            print(f"{Wh}├─ {Gr}{full_domain:<30} -> {ip}")
            found_subdomains.append(full_domain)
        except socket.gaierror:
            continue
        except Exception as e:
            continue
    
    if found_subdomains:
        print(f"{Wh}\n Total subdomains found: {len(found_subdomains)}")
    else:
        print(f"{Wh}├─ {Ye}No subdomains found")

@is_option
def Social_Media_OSINT():
    print(f"{Wh}\n Social Media OSINT Options:")
    print(f"{Wh} 1. Search by name")
    print(f"{Wh} 2. Search by email")
    print(f"{Wh} 3. Search by username")
    
    choice = input(f"\n{Wh} Select option (1-3) : {Gr}")
    
    if choice == '1':
        name = input(f"{Wh} Enter full name : {Gr}")
        print(f"{Wh}\n Searching for {name} on social media...")
        
        # Generate search URLs
        search_urls = [
            f"https://www.google.com/search?q={name}+site:facebook.com",
            f"https://www.google.com/search?q={name}+site:twitter.com",
            f"https://www.google.com/search?q={name}+site:instagram.com",
            f"https://www.google.com/search?q={name}+site:linkedin.com",
            f"https://www.google.com/search?q={name}+site:tiktok.com",
            f"https://www.google.com/search?q={name}+site:youtube.com",
            f"https://www.google.com/search?q={name}+site:reddit.com",
            f"https://www.google.com/search?q={name}+site:pinterest.com",
        ]
        
        print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
        print(f" {Wh}║         {Gr}NAME SEARCH RESULTS                       {Wh}║")
        print(f" {Wh}╚════════════════════════════════════════════════════╝")
        
        for url in search_urls:
            print(f"{Wh}├─ {Cy}{url}")
    
    elif choice == '2':
        email = input(f"{Wh} Enter email : {Gr}")
        print(f"{Wh}\n Searching for {email} on social media...")
        
        # Similar to username search but with email
        username = email.split('@')[0]
        search_urls = [
            f"https://www.facebook.com/search/top?q={email}",
            f"https://twitter.com/search?q={email}",
            f"https://www.instagram.com/{username}/",
            f"https://github.com/search?q={email}",
            f"https://www.google.com/search?q={email}",
        ]
        
        print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
        print(f" {Wh}║         {Gr}EMAIL SEARCH RESULTS                      {Wh}║")
        print(f" {Wh}╚════════════════════════════════════════════════════╝")
        
        for url in search_urls:
            print(f"{Wh}├─ {Cy}{url}")
    
    elif choice == '3':
        username = input(f"{Wh} Enter username : {Gr}")
        # Reuse username tracker but with more options
        Username_Track_Advanced()
    
    else:
        print(f"{Re} Invalid option")

@is_option
def showIP():
    try:
        # Multiple IP sources for accuracy
        respone1 = requests.get('https://api.ipify.org/')
        respone2 = requests.get('https://icanhazip.com/')
        respone3 = requests.get('https://ifconfig.me/ip')
        
        Show_IP1 = respone1.text.strip()
        Show_IP2 = respone2.text.strip()
        Show_IP3 = respone3.text.strip()
        
        print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
        print(f" {Wh}║         {Gr}YOUR PUBLIC IP INFORMATION                {Wh}║")
        print(f" {Wh}╚════════════════════════════════════════════════════╝")
        
        print(f"\n {Wh}[{Gr}1{Wh}] IP Address (ipify)  : {Gr}{Show_IP1}")
        print(f" {Wh}[{Gr}2{Wh}] IP Address (icanhaz) : {Gr}{Show_IP2}")
        print(f" {Wh}[{Gr}3{Wh}] IP Address (ifconfig): {Gr}{Show_IP3}")
        
        # Get location of your IP
        req_api = requests.get(f"http://ipwho.is/{Show_IP1}")
        ip_data = json.loads(req_api.text)
        
        print(f"\n {Wh}┌─[ YOUR IP GEOLOCATION ]")
        print(f" {Wh}├─ Country     : {Gr}{ip_data.get('country', 'N/A')}")
        print(f" {Wh}├─ City        : {Gr}{ip_data.get('city', 'N/A')}")
        print(f" {Wh}├─ ISP         : {Gr}{ip_data.get('connection', {}).get('isp', 'N/A')}")
        
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def Geolocation_Maps():
    location = input(f"\n {Wh}Enter location (city, country or coordinates) : {Gr}")
    
    try:
        # Use OpenStreetMap Nominatim for geocoding
        params = {
            'q': location,
            'format': 'json',
            'limit': 1
        }
        
        response = requests.get('https://nominatim.openstreetmap.org/search', params=params, headers={'User-Agent': 'DARKX-Tracker'})
        
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            lat = float(data['lat'])
            lon = float(data['lon'])
            
            print(f"\n {Wh}╔════════════════════════════════════════════════════╗")
            print(f" {Wh}║         {Gr}GEOLOCATION MAP                           {Wh}║")
            print(f" {Wh}╚════════════════════════════════════════════════════╝")
            
            print(f"{Wh}\n Location: {Gr}{data['display_name']}")
            print(f"{Wh} Latitude: {Gr}{lat}")
            print(f"{Wh} Longitude: {Gr}{lon}")
            
            # Create map
            m = folium.Map(location=[lat, lon], zoom_start=12)
            folium.Marker([lat, lon], popup=location).add_to(m)
            
            # Save map
            map_file = 'location_map.html'
            m.save(map_file)
            
            print(f"{Wh}\n Map saved as {map_file}")
            open_map = input(f"{Wh} Open map in browser? (y/n) : {Gr}")
            
            if open_map.lower() == 'y':
                webbrowser.open(map_file)
        else:
            print(f"{Re} Location not found")
            
    except Exception as e:
        print(f"{Re} Error: {e}")

@is_option
def Data_Export():
    print(f"{Wh}\n Export Options:")
    print(f"{Wh} 1. Export IP history to CSV")
    print(f"{Wh} 2. Export Phone history to CSV")
    print(f"{Wh} 3. Export Username history to CSV")
    print(f"{Wh} 4. Export all data to CSV")
    
    choice = input(f"\n{Wh} Select option (1-4) : {Gr}")
    
    conn = sqlite3.connect('darkx_tracker.db')
    
    if choice == '1':
        df = pd.read_sql_query("SELECT * FROM ip_history", conn)
        df.to_csv('ip_history.csv', index=False)
        print(f"{Gr} IP history exported to ip_history.csv")
    
    elif choice == '2':
        df = pd.read_sql_query("SELECT * FROM phone_history", conn)
        df.to_csv('phone_history.csv', index=False)
        print(f"{Gr} Phone history exported to phone_history.csv")
    
    elif choice == '3':
        df = pd.read_sql_query("SELECT * FROM username_history", conn)
        df.to_csv('username_history.csv', index=False)
        print(f"{Gr} Username history exported to username_history.csv")
    
    elif choice == '4':
        with pd.ExcelWriter('darkx_data.xlsx') as writer:
            pd.read_sql_query("SELECT * FROM ip_history", conn).to_excel(writer, sheet_name='IP History')
            pd.read_sql_query("SELECT * FROM phone_history", conn).to_excel(writer, sheet_name='Phone History')
            pd.read_sql_query("SELECT * FROM username_history", conn).to_excel(writer, sheet_name='Username History')
        print(f"{Gr} All data exported to darkx_data.xlsx")
    
    conn.close()

@is_option
def Webhook_Integration():
    webhook_url = input(f"\n {Wh}Enter Discord/Slack webhook URL : {Gr}")
    
    print(f"{Wh}\n Webhook Options:")
    print(f"{Wh} 1. Send IP tracking result")
    print(f"{Wh} 2. Send phone tracking result")
    print(f"{Wh} 3. Send username tracking result")
    
    choice = input(f"\n{Wh} Select option (1-3) : {Gr}")
    
    if choice == '1':
        ip = input(f"{Wh} Enter IP to send : {Gr}")
        data = load_from_db('ip_history', ip)
        if data:
            message = {
                "content": f"**IP Tracking Result**\nIP: {ip}\nCountry: {data.get('country', 'N/A')}\nCity: {data.get('city', 'N/A')}\nISP: {data.get('connection', {}).get('isp', 'N/A')}"
            }
            response = requests.post(webhook_url, json=message)
            if response.status_code == 204:
                print(f"{Gr} Message sent successfully")
            else:
                print(f"{Re} Failed to send message")
        else:
            print(f"{Ye} No data found for this IP")
    
    # Similar for other options...

# ---------- MENU ----------
options = [
    {'num': 1, 'text': 'IP Tracker (Advanced)', 'func': IP_Track_Advanced},
    {'num': 2, 'text': 'Show My IP', 'func': showIP},
    {'num': 3, 'text': 'Phone Number Tracker (Advanced)', 'func': Phone_Track_Advanced},
    {'num': 4, 'text': 'Username Tracker (Advanced)', 'func': Username_Track_Advanced},
    {'num': 5, 'text': 'MAC Address Lookup', 'func': mac_lookup},
    {'num': 6, 'text': 'Website Analyzer (Advanced)', 'func': Website_Analyzer},
    {'num': 7, 'text': 'Reverse IP Lookup', 'func': reverse_ip},
    {'num': 8, 'text': 'BIN (Credit Card) Lookup', 'func': bin_lookup},
    {'num': 9, 'text': 'Email Tracker', 'func': Email_Tracker},
    {'num': 10, 'text': 'Port Scanner', 'func': Port_Scanner},
    {'num': 11, 'text': 'DNS Enumeration', 'func': DNS_Enumeration},
    {'num': 12, 'text': 'Subdomain Finder', 'func': Subdomain_Finder},
    {'num': 13, 'text': 'IP Range Scanner', 'func': IP_Range_Scan},
    {'num': 14, 'text': 'Social Media OSINT', 'func': Social_Media_OSINT},
    {'num': 15, 'text': 'Hash Cracker', 'func': Hash_Cracker},
    {'num': 16, 'text': 'Metadata Extractor', 'func': Metadata_Extractor},
    {'num': 17, 'text': 'Geolocation Maps', 'func': Geolocation_Maps},
    {'num': 18, 'text': 'Data Export', 'func': Data_Export},
    {'num': 19, 'text': 'Webhook Integration', 'func': Webhook_Integration},
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
    # Display in two columns for better organization
    half = len(options) // 2
    for i in range(half):
        opt1 = options[i]
        opt2 = options[i + half] if i + half < len(options) else None
        text += f'{Wh}[ {opt1["num"]:2} ] {Gr}{opt1["text"]:<30}'
        if opt2:
            text += f'{Wh}[ {opt2["num"]:2} ] {Gr}{opt2["text"]:<30}\n'
        else:
            text += '\n'
    return text

def option():
    clear()
    stderr.writelines(f"""
{Wh}╔════════════════════════════════════════════════════════════════╗
{Wh}║      {Gr}██████╗  █████╗ ██████╗ ██╗  ██╗   ██╗   ██╗██████╗  {Wh}║
{Wh}║      {Gr}██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝   ██║   ██║██╔══██╗ {Wh}║
{Wh}║      {Gr}██║  ██║███████║██████╔╝█████╔╝    ██║   ██║██████╔╝ {Wh}║
{Wh}║      {Gr}██║  ██║██╔══██║██╔══██╗██╔═██╗    ╚██╗ ██╔╝██╔══██╗ {Wh}║
{Wh}║      {Gr}██████╔╝██║  ██║██║  ██║██║  ██╗    ╚████╔╝ ██████╔╝ {Wh}║
{Wh}║      {Gr}╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═══╝  ╚═════╝  {Wh}║
{Wh}║                    {Cy}ADVANCED TRACKER PRO                      {Wh}║
{Wh}║               {Ye}19 Modules • Database • Webhook                {Wh}║
{Wh}╚════════════════════════════════════════════════════════════════╝
    """)
    stderr.writelines(f"\n\n{option_text()}")

def run_banner():
    clear()
    time.sleep(1)
    stderr.writelines(f"""{Wh}
╔════════════════════════════════════════════════════════════════╗
║                      {Gr}DARKX TRACKER PRO                        {Wh}║
║                  {Cy}The Ultimate Tracking Suite                 {Wh}║
║                                                                ║
║        {Wh}[ {Gr}IP • Phone • Username • Email • Website {Wh}]         ║
║        {Wh}[ {Gr}DNS • Ports • Subdomains • Metadata {Wh}]           ║
║        {Wh}[ {Gr}OSINT • Maps • Export • Webhook {Wh}]              ║
║                                                                ║
║              {Mage}Initializing Advanced Modules...               {Wh}║
╚════════════════════════════════════════════════════════════════╝
    """)
    time.sleep(1.5)

def check_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        'requests', 'phonenumbers', 'dnspython', 'python-whois',
        'beautifulsoup4', 'pandas', 'scapy', 'netifaces', 'paramiko',
        'python-nmap', 'folium', 'pillow', 'pypdf2', 'openpyxl'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"{Ye} Missing dependencies: {', '.join(missing)}")
        install = input(f"{Wh} Install missing dependencies? (y/n) : {Gr}")
        if install.lower() == 'y':
            for package in missing:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"{Gr} Dependencies installed. Please restart the tool.")
            exit()

def main():
    check_dependencies()
    clear()
    option()
    time.sleep(1)
    try:
        opt = int(input(f"{Wh}\n [ + ] {Gr}Select Option [0-19] : {Wh}"))
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
