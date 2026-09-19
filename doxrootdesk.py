import socket
import sys

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(1)
    print("\n[*] Sunucu (Agent) modu başlatıldı. 5000 portu dinleniyor...")
    print("[*] Bağlantı bekleniyor...")
    
    client_socket, addr = server_socket.accept()
    print(f"\n[+] {addr[0]} adresinden bir bağlantı isteği geldi!")
    
    # Karşı taraftan gelen istek sinyalini al
    try:
        req = client_socket.recv(1024).decode('utf-8')
        if "BAGLANTI_ISTEGI" in req:
            cevap = input("Bu bağlantıyı onaylıyor musun? (E/H): ").strip().upper()
            
            if cevap == 'E':
                client_socket.send(b"ERISIM_ONAYLANDI")
                print("\n[OK] Bağlantı onaylandı! Oturum aktif.")
                print("Çıkış yapmak için 'q' yazabilirsiniz.")
                
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    print(f"\n[Karşı Taraftan Gelen]: {data.decode('utf-8', errors='ignore')}")
            else:
                client_socket.send(b"ERISIM_REDDEDILDI")
                print("\n[-] Bağlantı reddedildi.")
    except Exception as e:
        print(f"[-] Hata oluştu: {e}")
    finally:
        client_socket.close()
        server_socket.close()
        print("[*] Oturum sonlandırıldı.")

def start_client():
    target_ip = input("\nBağlanılacak hedef IP adresini girin: ").strip()
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"[*] {target_ip}:{port} adresine bağlanılıyor...")
        client_socket.connect((target_ip, port))
        
        # Hedef cihaza bağlantı isteği gönder
        client_socket.send(b"BAGLANTI_ISTEGI")
        print("[*] İstek gönderildi, karşı taraftan onay bekleniyor...")
        
        response = client_socket.recv(1024).decode('utf-8')

        if "ERISIM_ONAYLANDI" in response:
            print("\n[BAŞARILI] Karşı taraf bağlantıyı onayladı!")
            print("Mesaj göndermek için yazın. Çıkış için 'q' tuşlayın.")
            
            while True:
                mesaj = input("Gönderilecek Mesaj: ")
                if mesaj.lower() == 'q':
                    break
                client_socket.send(mesaj.encode('utf-8'))
        else:
            print("\n[RED] Karşı taraf bağlantı isteğini reddetti.")
            
    except Exception as e:
        print(f"[-] Bağlantı hatası: {e}")
    finally:
        client_socket.close()
        print("[*] Bağlantı kapatıldı.")

if __name__ == "__main__":
    while True:
        print("\n==============================")
        print("  ÖZEL UZAKTAN YÖNETİM ARACI  ")
        print("==============================")
        print("1. Hedef Ol (Bağlantı Bekle / Agent)")
        print("2. Bağlanıcı Ol (Yönetici / Client)")
        print("3. Çıkış")
        
        secim = input("\nSeçiminiz (1, 2 veya 3): ").strip()
        
        if secim == '1':
            start_server()
            break
        elif secim == '2':
            start_client()
            break
        elif secim == '3':
            print("Çıkış yapılıyor...")
            sys.exit()
        else:
            print("Geçersiz seçim, lütfen 1, 2 veya 3 girin.")
