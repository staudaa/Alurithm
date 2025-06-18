import os
import pandas as pd

file_path = r"D:\COLLEGE LIFE\Semester 2\ALGORITMA DAN PEMROGRAMAN II\PROJECT ALGO PYFIGLET\Alurithm\db\accounts.csv"

def accountData():
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        df = pd.DataFrame(columns=['Index', 'Username', 'Password'])
        df.to_csv(file_path, index=False)
        return df
    
    return pd.read_csv(file_path, dtype={'Index': int,'Username': str, 'Password': str})

def login(errorMsg=False):
    os.system('cls')
    
    if errorMsg:
        print(f"\n{' ' * 10} {errorMsg} \n")
        
    print("-"*80)
    print(f"|{' ' * 78}|")
    print(f"|{'LOGIN':^78}|")
    print(f"|{' ' * 78}|")
    print("-"*80)
    
    while True:
        username = input("\nMasukkan Username anda : ").strip()
        password = input("Masukkan Password anda : ").strip()
        
        accounts = accountData()
        account = accounts[accounts['Username'] == username]
        
        if account.empty or account.iloc[0]["Password"].strip() != password:
            print(f"Password mismatch: '{account.iloc[0]['Password']}' != '{password}'")
            return login("Maaf Username Atau Password Yang Anda Berikan Salah!")
        break
    return [account.iloc[0]["Username"]]
  
def addAccount(username=None, password=None):
    accounts = accountData()
    next_index = accounts.shape[0] + 1
    
    new_account = pd.DataFrame({
        'Index': [next_index],
        'Username': [username],
        'Password': [str(password).strip()]
    })
    
    if not os.path.isfile(file_path):
        new_account.to_csv(file_path, mode='w', header=True, index=False)
    else:
        new_account.to_csv(file_path, mode='a', header=False, index=False)
    return [username]

def register(errorMsg=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if errorMsg:
        print(f"\n{' ' * 10} {errorMsg} \n")
        
    print("-" * 80)
    print(f"|{' ' * 78}|")
    print(f"|{'REGISTER':^78}|")
    print(f"|{' ' * 78}|")
    print("-" * 80)
    
    while True:
        username = input("\nMasukkan Username (minimal 3 character!): ").strip()
        password = input("Masukkan Password (minimal 5 character!): ").strip()
        os.system('cls' if os.name == 'nt' else 'clear')
        confirmedPassword = input(" Konfirmasi Ulang Password: ").strip()
        
        if not username:
            return register("Username tidak boleh hanya berupa spasi!")
        
        if len(username) < 3:
            return register("Username Akun Minimal 3 character!")
            
        accounts = accountData()
        
        if not accounts[accounts['Username'] == username].empty:
            return register("Username Sudah Digunakan!")
        
        if not password:
            return register("Password tidak boleh hanya berupa spasi!")

        if len(password) < 5 :
            return register("Password Akun Minimal 5 character!")
        
        if password != confirmedPassword:
            return register("Konfirmasi Ulang Password Berbeda Dengan Password Awal!")
        
        return addAccount(username, password)