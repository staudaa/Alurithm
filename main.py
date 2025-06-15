import csv
import os
from Logic_BFS_DFS import graf_labirin
from auth import login, register
from leaderboard import add_score, display_leaderboard
import pandas as pd
import time

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_soal():
    soal_map = {'Easy': [], 'Medium': [], 'Hard': []}
    with open('D:\COLLEGE LIFE\Semester 2\Project Algo II non-fix\Alurithm\db\soal.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            soal_map[row['Tingkat']].append(row)
    return soal_map

def tingkat_node(node):
    if node in ['IN']:
        return 'Easy'
    elif node in ['B1', 'S1', 'L1']:
        return 'Medium'
    elif node in ['S2', 'L2', 'L3']:
        return 'Hard'
    return None

def main_game(username):
    
    soal_map = load_soal()
    posisi = 'IN'
    riwayat = [posisi]
    nyawa = 3
    persentase = 100
    skor_sementara = 0
    hasil = ' '
    waktu_mulai = time.time()

    while posisi != 'OUT':
        bersihkan_layar()
        tingkat = tingkat_node(posisi)
        if not soal_map[tingkat]:
            print(f"Tidak ada soal tersedia untuk tingkat {tingkat}.")
            break
        
        soal = soal_map[tingkat].pop(0)
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
            # print(f"\nAnda mendapatkan {bobot_soal} poin \nTotal skor Anda sekarang: {skor_sementara} poin")
        else:
            hasil = 'salah'
            print("Jawaban Salah! ")
            persentase -= 10
            if persentase <= 0:
                print("\nGame over!!! \nAnda telah kehilangan kesempatan untuk menjawab soal.")
                break

        if posisi == 'L1' and hasil == 'salah':
            nyawa -= 1
            print(f"Nyawa kamu tersisa: {nyawa}")
            if nyawa == 0:
                print("Nyawa Kamu Habis! Game over!!!")
                break
            continue
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
        print("\nSelamat! Kamu telah mencapai tujuan akhir!")
        print(f"Skor akhir anda: {skor_akhir} poin")

        add_score(username, skor_akhir)
        print("\nBerikut adalah leaderboard terbaru:")
        display_leaderboard()
    
    print(f"\nTotal waktu bermain: {menit} menit {detik} detik")      
    print("\nRute yang ditempuh:")
    print(" → ".join(riwayat))

    input("\nTekan Enter untuk kembali ke menu...")
        
def pembulatan_5 (n):
    return round(n / 5) * 5

def autentikasi(username):
    while True:
        bersihkan_layar()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Selamat datang, {username}!")
        print("\nMenu:")
        print("1. Lihat Leaderboard")
        print("2. Mulai Permainan")
        print("3. Logout")
        pilihan = input("Masukkan pilihan (1/2/3): ").strip()
        if pilihan == '1':
            bersihkan_layar()
            display_leaderboard()
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == '2':
            bersihkan_layar()
            print("1. Mulai")
            print("2. Kembali")
            menu = input("Masukkan pilihan menu (1/2) : ")
            if menu == "1" : 
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
        print("Selamat datang di Alurithm! \nPermainan labirin berbasis soal Algoritma dan Pemrograman Dasar")
        print("\nPilih opsi:")
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
            print("Terima kasih sudah mencoba. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == '__main__':
    main()
