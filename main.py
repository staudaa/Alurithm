import csv
import os
import time
import random
import pyfiglet
import shutil
import pandas as pd
from Logic_BFS_DFS import graf_labirin
from auth import login, register
from leaderboard import add_score, display_leaderboard, cari_username
from visualisasi import visual
from colorama import Fore, Style, init


init()

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered_figlet(text):
    f = pyfiglet.Figlet(font='doom')  
    ascii_art = f.renderText(text)
    terminal_width = shutil.get_terminal_size().columns

    for line in ascii_art.splitlines():
        print(Fore.MAGENTA + line.center(terminal_width) + Style.RESET_ALL)
    
def load_soal():
    soal_map = {'Easy': [], 'Medium': [], 'Hard': []}
    with open('D:\COLLEGE LIFE\Semester 2\ALGORITMA DAN PEMROGRAMAN II\PROJECT ALGO PYFIGLET\Alurithm\db\soal.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            soal_map[row['Tingkat']].append(row)
    soal_tampilkan = {}
    for tingkat in soal_map:
        soal_tampilkan[tingkat] = random.sample(soal_map[tingkat], len(soal_map[tingkat]))
    return soal_map, soal_tampilkan

def ambil_soal(tingkat, soal_tampilkan):
    if not soal_tampilkan[tingkat]:
        return None
    return soal_tampilkan[tingkat].pop(0)

def tingkat_node(node):
    if node in ['IN']:
        return 'Easy'
    elif node in ['B1', 'S1', 'L1']:
        return 'Medium'
    elif node in ['S2', 'L2', 'L3']:
        return 'Hard'
    return None

def main_game(username): 
        soal_map, soal_tampilkan = load_soal()
        posisi = 'IN'
        riwayat = [posisi]
        nyawa = 3
        persentase = 100
        skor_sementara = 0
        hasil = ' '
        waktu_mulai = time.time()

        while posisi != 'OUT':
            bersihkan_layar()
            visual(riwayat)
            if posisi == 'L1' and hasil == 'salah':
                print(f"Nyawa kamu: {nyawa}")
            tingkat = tingkat_node(posisi)
            if not soal_tampilkan[tingkat]:
                break
            
            soal = ambil_soal(tingkat, soal_tampilkan)
            if soal is None:
                soal_tampilkan[tingkat] = random.sample(soal_map[tingkat], len(soal_map[tingkat]))
                soal = ambil_soal(tingkat, soal_tampilkan)
                
            print(f"\nLokasi: {posisi} | Tingkat: {tingkat}")
            print(f"{soal['Soal']}")

            if soal['Tipe'] == 'PG':
                print(f"A. {soal['Opsi_A']}")
                print(f"B. {soal['Opsi_B']}")
                print(f"C. {soal['Opsi_C']}")
                print(f"D. {soal['Opsi_D']}")
                jawaban = input("Jawaban Anda (A/B/C/D): ").strip().upper()
                benar = jawaban == soal['Jawaban'].upper()
            elif soal['Tipe'] == 'Esai':
                jawaban = input("Jawaban Anda: ").strip()
                benar = jawaban.lower() == soal['Jawaban'].lower()
            else:
                print("Tipe soal tidak dikenali.")
                break
            
            if benar:
                hasil = 'benar'
                print("Jawaban Benar! ")
                bobot_soal = int(soal['Poin'])
                poin = int(bobot_soal * (persentase / 100))
                skor_sementara += poin
            else:
                hasil = 'salah'
                print("Jawaban Salah! ")
                persentase -= 10
                if persentase <= 0:
                    bersihkan_layar()
                    print_centered_figlet("GAME OVER!")
                    print("Akurasimu turun hingga 0%.")
                    break

            if posisi == 'L1' and hasil == 'salah':
                nyawa -= 1
                if nyawa == 0:
                    bersihkan_layar()
                    print_centered_figlet("GAME OVER!")
                    print(f"\nKamu telah kehilangan semua nyawa.")
                    break
            elif posisi == 'L1' and hasil == 'benar':
                nyawa = 3
            if hasil in graf_labirin[posisi]:
                posisi = graf_labirin[posisi][hasil]
                riwayat.append(posisi)
            else:
                print("Tidak ada jalur lanjutan.")
                break
        
        waktu_selesai = time.time()
        durasi = int(waktu_selesai - waktu_mulai)
        menit = durasi // 60
        detik = durasi % 60
        waktu_str = f"{menit} menit {detik} detik" 
        
        skor_maks = 100
        total_node_terpendek = 3
        total_node_dilalui = len(riwayat)
        efisiensi = total_node_terpendek / total_node_dilalui
        skor_akhir = int(skor_sementara * efisiensi)
        
        if len(riwayat) == 3:
            skor_akhir = skor_maks
        elif len(riwayat) > 3 and persentase == 90:
            skor_akhir = skor_maks - 15
        elif len(riwayat) > 3 and persentase == 80:
            skor_akhir = skor_maks - 30
        else:
            skor_maks = 50
            skor_akhir = min(pembulatan_5(skor_akhir), skor_maks)
        if posisi == 'OUT':
            bersihkan_layar()
            print_centered_figlet("SELAMAT!")
            print("\nKamu telah mencapai tujuan akhir!")
            print(f"Skor akhir anda: {skor_akhir} poin")
            input("\nTekan Enter untuk melanjutkan...")
            bersihkan_layar()
            add_score(username, skor_akhir, waktu_str)
            print("\nBerikut adalah leaderboard terbaru:")
            display_leaderboard()
        
        print(f"\nTotal waktu bermain: {menit} menit {detik} detik")      
        print("\nRute yang ditempuh:")
        print(" → ".join(riwayat))
        visual(riwayat)

        input("\nTekan Enter untuk kembali ke menu...")
        
def pembulatan_5 (n):
    return round(n / 5) * 5

def autentikasi(username):
    while True:
        bersihkan_layar()
        print_centered_figlet("ALURITHM")
        print(f"Selamat datang, {username}!")
        print("\nMenu:")
        print("1. Lihat Leaderboard")
        print("2. Mulai Permainan")
        print("3. Logout")
        pilihan = input("Masukkan pilihan (1/2/3): ").strip()
        if pilihan == '1':
            bersihkan_layar()
            display_leaderboard()
            cari = input('\nKetik "C" untuk mencari username di leaderboard\n\nTekan Enter untuk kembali ke menu\n\nMasukkan pilihan: ').strip()
            if cari == 'c' or cari == 'C':
                bersihkan_layar()
                target = input("Masukkan username yang ingin dicari untuk melihat skor dan waktu bermain: ").strip()
                bersihkan_layar()
                cari_username(target)                
                input("\nTekan Enter untuk kembali ke menu...")
            else:
                bersihkan_layar()
        elif pilihan == '2':
            bersihkan_layar()
            print_centered_figlet("ALURITHM")
            print("1. Mulai")
            print("2. Kembali")
            menu = input("Masukkan pilihan menu (1/2) : ")
            if menu == "1" :
                bersihkan_layar() 
                main_game(username)
            elif menu == "2" :
                continue
        elif pilihan == '3':
            bersihkan_layar()
            print("Anda telah logout.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def main():
    while True:
        bersihkan_layar()
        print_centered_figlet("ALURITHM")
        print("Selamat datang di Alurithm! \nPermainan labirin berbasis soal Algoritma dan Pemrograman Dasar")
        print("\nPilih Menu:")
        print("1. Register")
        print("2. Login")
        print("3. Keluar")
        pilihan = input("Masukkan pilihan (1/2/3): ").strip()
        if pilihan == '1':
            register()
        elif pilihan == '2':
            username = login()
            if username:
                autentikasi(username[0])  
        elif pilihan == '3':
            bersihkan_layar()
            print_centered_figlet("TERIMA KASIH!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == '__main__':
    main()
