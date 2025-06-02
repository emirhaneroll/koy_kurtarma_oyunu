from typing import List, Optional
import sys
import os

class Item:
    def __init__(self, name: str, power: int = 0):
        self.name = name
        self.power = power

    def __str__(self):
        return f"{self.name} (Güç: {self.power})"

class Node:
    def __init__(self, item: Item):
        self.item = item
        self.left = None
        self.right = None
        self.height = 1  # AVL için yükseklik bilgisi eklendi

class AVLTree:
    def __init__(self):
        self.root = None
        self.items = []  # Öğeleri takip etmek için liste eklendi

    def get_height(self, node: Node) -> int:
        if not node:
            return 0
        return node.height

    def get_balance(self, node: Node) -> int:
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y: Node) -> Node:
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1

        return x

    def left_rotate(self, x: Node) -> Node:
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1

        return y

    def insert(self, item: Item):
        self.root = self._insert(self.root, item)
        self.items.append(item)  # Öğeyi listeye ekle

    def _insert(self, node: Node, item: Item) -> Node:
        if not node:
            return Node(item)

        if item.name < node.item.name:
            node.left = self._insert(node.left, item)
        else:
            node.right = self._insert(node.right, item)

        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1

        balance = self.get_balance(node)

        # Sol Sol Durumu
        if balance > 1 and item.name < node.left.item.name:
            return self.right_rotate(node)

        # Sağ Sağ Durumu
        if balance < -1 and item.name > node.right.item.name:
            return self.left_rotate(node)

        # Sol Sağ Durumu
        if balance > 1 and item.name > node.left.item.name:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Sağ Sol Durumu
        if balance < -1 and item.name < node.right.item.name:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def search(self, item_name: str) -> Optional[Item]:
        return self._search(self.root, item_name)

    def _search(self, node: Node, item_name: str) -> Optional[Item]:
        if not node:
            return None

        if item_name == node.item.name:
            return node.item
        elif item_name < node.item.name:
            return self._search(node.left, item_name)
        else:
            return self._search(node.right, item_name)

    def delete(self, item_name: str) -> bool:
        self.root = self._delete(self.root, item_name)
        # Listeden öğeyi kaldır
        self.items = [item for item in self.items if item.name != item_name]
        return True

    def _delete(self, node: Node, item_name: str) -> Optional[Node]:
        if not node:
            return None

        if item_name < node.item.name:
            node.left = self._delete(node.left, item_name)
        elif item_name > node.item.name:
            node.right = self._delete(node.right, item_name)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self._get_min_value_node(node.right)
            node.item = temp.item
            node.right = self._delete(node.right, temp.item.name)

        if not node:
            return None

        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        balance = self.get_balance(node)

        # Sol Sol Durumu
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        # Sol Sağ Durumu
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Sağ Sağ Durumu
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        # Sağ Sol Durumu
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def _get_min_value_node(self, node: Node) -> Node:
        current = node
        while current.left:
            current = current.left
        return current

class Village:
    def __init__(self, name: str):
        self.name = name
        self.inventory = AVLTree()  # BST yerine AVLTree kullanıldı
        self.is_liberated = False

    def add_item(self, item: Item):
        self.inventory.insert(item)

    def has_item(self, item_name: str) -> bool:
        return self.inventory.search(item_name) is not None

class Inventory:
    def __init__(self, max_capacity: int = 10):
        self.max_capacity = max_capacity
        self.items = []
        self.bst = AVLTree()  # BST yerine AVLTree kullanıldı

    def push(self, item: Item) -> bool:
        if len(self.items) >= self.max_capacity:
            return False
        self.items.append(item)
        self.bst.insert(item)
        return True

    def pop(self) -> Optional[Item]:
        if not self.items:
            return None
        item = self.items.pop()
        self.bst.delete(item.name)  # BST'den silme işlemi eklendi
        return item

    def use_item(self, item_name: str) -> bool:
        # Öğeyi büyük/küçük harf duyarlılığı olmadan ara
        found_item = next((item for item in self.items if item.name.lower() == item_name.lower()), None)
        if found_item:
            self.items.remove(found_item)
            self.bst.delete(found_item.name)
            return True
        return False

class Game:
    def __init__(self):
        self.villages = []
        self.inventory = Inventory()
        self.current_village_index = 0
        self.initialize_villages()

    def initialize_villages(self):
        # 7 köyü oluştur
        village_names = ["Yeşilvadi", "Gümüşköy", "Altınşehir", "Demirtepe", 
                        "Kristalköy", "Zümrütvadi", "Elmasşehir"]
        
        # Tüm öğeleri tanımla
        all_items = [
            Item("Kılıç", 10),
            Item("İksir", 5),
            Item("Harita", 2),
            Item("Balta", 8),
            Item("Altın", 15),
            Item("Yiyecek", 3),
            Item("Bakır", 4),
            Item("Gümüş", 6),
            Item("Kalkan", 7),
            Item("Zırh", 12),
            Item("Anahtar", 1),
            Item("Meşale", 2),
            Item("Ok-Yay", 9)
        ]
        
        # Her köy için özel öğe kombinasyonları
        village_items = [
            [all_items[0], all_items[5], all_items[8]],  # Yeşilvadi: Kılıç, Yiyecek, Kalkan
            [all_items[1], all_items[6], all_items[9]],  # Gümüşköy: İksir, Bakır, Zırh
            [all_items[2], all_items[7], all_items[10]], # Altınşehir: Harita, Gümüş, Anahtar
            [all_items[3], all_items[8], all_items[11]], # Demirtepe: Balta, Kalkan, Meşale
            [all_items[4], all_items[9], all_items[12]], # Kristalköy: Altın, Zırh, Ok-Yay
            [all_items[5], all_items[10], all_items[0]], # Zümrütvadi: Yiyecek, Anahtar, Kılıç
            [all_items[6], all_items[11], all_items[1]]  # Elmasşehir: Bakır, Meşale, İksir
        ]
        
        for i, name in enumerate(village_names):
            village = Village(name)
            # Her köye 3 öğe ekle
            for item in village_items[i]:
                village.add_item(item)
            self.villages.append(village)

    def show_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')  # Terminali temizle
            print("\n=== Köy Kurtarma Oyunu ===")
            print("1. Köyleri Listele")
            print("2. Çantayı Görüntüle")
            print("3. Köy Kurtar")
            print("4. Öğe Kullan/Çıkar")
            print("5. Arama Yap")
            print("6. İlerleme Durumu")
            print("7. Çıkış")
            
            choice = input("\nSeçiminiz (1-7): ")
            
            if choice == "1":
                self.list_villages()
                input("\nDevam etmek için Enter'a basın...")
            elif choice == "2":
                self.show_inventory()
                input("\nDevam etmek için Enter'a basın...")
            elif choice == "3":
                self.liberate_village()
                input("\nDevam etmek için Enter'a basın...")
            elif choice == "4":
                self.use_item()
                input("\nDevam etmek için Enter'a basın...")
            elif choice == "5":
                self.search_item()
                input("\nDevam etmek için Enter'a basın...")
            elif choice == "6":
                self.show_progress()
                input("\nDevam etmek için Enter'a basın...")
            elif choice == "7":
                print("Oyun sonlandırılıyor...")
                sys.exit()
            else:
                print("Geçersiz seçim!")
                input("\nDevam etmek için Enter'a basın...")

    def list_villages(self):
        print("\n=== Köyler ===")
        for i, village in enumerate(self.villages, 1):
            status = "Kurtarıldı" if village.is_liberated else "Kurtarılmadı"
            items_str = ", ".join([item.name for item in village.inventory.items])
            print(f"{i}. {village.name} - {status}")
            print(f"   Öğeler: {items_str}")
            # Son 3 köy için özel şartları göster
            if i == 5 and not village.is_liberated:
                print("   Köyü kurtarmak için Kılıç ve Zırh gerekiyor!")
            elif i == 6 and not village.is_liberated:
                print("   Köyü kurtarmak için Ok-Yay ve Anahtar gerekiyor!")
            elif i == 7 and not village.is_liberated:
                print("   Köyü kurtarmak için Altın ve Kalkan gerekiyor!")
            print()  # Boş satır ekle

    def show_inventory(self):
        print("\n=== Çanta ===")
        if not self.inventory.items:
            print("Çanta boş!")
        else:
            for item in self.inventory.items:
                print(item)

    def liberate_village(self):
        if self.current_village_index >= len(self.villages):
            print("Tüm köyler kurtarıldı!")
            return

        current_village = self.villages[self.current_village_index]
        print(f"\n{current_village.name} köyünü kurtarmaya çalışıyorsunuz...")
        
        # Son 3 köy için özel şartlar
        if self.current_village_index == 4:  # 5. köy
            required_items = ["Kılıç", "Zırh"]
            missing_items = [item for item in required_items 
                           if not any(inv_item.name.lower() == item.lower() for inv_item in self.inventory.items)]
            
            if missing_items:
                print(f"Bu köyü kurtarmak için şu öğelere ihtiyacınız var: {', '.join(missing_items)}")
                return
                
            print("Kılıç ve Zırh kontrol ediliyor...")
            # Öğeleri kullan
            for item_name in required_items:
                found_item = next((item for item in self.inventory.items if item.name.lower() == item_name.lower()), None)
                if found_item:
                    self.inventory.use_item(found_item.name)
                    print(f"{found_item.name} kullanıldı.")
            
        elif self.current_village_index == 5:  # 6. köy
            required_items = ["Ok-Yay", "Anahtar"]
            missing_items = [item for item in required_items 
                           if not any(inv_item.name.lower() == item.lower() for inv_item in self.inventory.items)]
            
            if missing_items:
                print(f"Bu köyü kurtarmak için şu öğelere ihtiyacınız var: {', '.join(missing_items)}")
                return
                
            print("Ok-Yay ve Anahtar kontrol ediliyor...")
            # Öğeleri kullan
            for item_name in required_items:
                found_item = next((item for item in self.inventory.items if item.name.lower() == item_name.lower()), None)
                if found_item:
                    self.inventory.use_item(found_item.name)
                    print(f"{found_item.name} kullanıldı.")
            
        elif self.current_village_index == 6:  # 7. köy
            required_items = ["Altın", "Kalkan"]
            missing_items = [item for item in required_items 
                           if not any(inv_item.name.lower() == item.lower() for inv_item in self.inventory.items)]
            
            if missing_items:
                print(f"Bu köyü kurtarmak için şu öğelere ihtiyacınız var: {', '.join(missing_items)}")
                return
                
            print("Altın ve Kalkan kontrol ediliyor...")
            # Öğeleri kullan
            for item_name in required_items:
                found_item = next((item for item in self.inventory.items if item.name.lower() == item_name.lower()), None)
                if found_item:
                    self.inventory.use_item(found_item.name)
                    print(f"{found_item.name} kullanıldı.")

        # Köydeki öğeleri çantaya ekle
        for item in current_village.inventory.items:
            if not self.inventory.push(item):
                print("\nÇanta dolu! Bir öğe çıkarmalısınız.")
                print("\nÇantanızdaki öğeler:")
                for i, inv_item in enumerate(self.inventory.items, 1):
                    print(f"{i}. {inv_item}")
                item_to_remove = input("\nÇıkarmak istediğiniz öğenin adını girin: ").lower()
                found_item = next((item for item in self.inventory.items if item.name.lower() == item_to_remove), None)
                if found_item:
                    self.inventory.use_item(found_item.name)
                    self.inventory.push(item)
                    print(f"{found_item.name} çantadan çıkarıldı ve {item.name} eklendi.")
                else:
                    print("Öğe bulunamadı!")
                    return

        current_village.is_liberated = True
        self.current_village_index += 1
        print(f"{current_village.name} köyü başarıyla kurtarıldı!")
        
        # Son 3 köy için kullanılan öğeleri belirten mesajlar
        if self.current_village_index == 5:  # 5. köy kurtarıldıktan sonra
            print("Kılıç ve Zırh kullanıldı.")
        elif self.current_village_index == 6:  # 6. köy kurtarıldıktan sonra
            print("Ok-Yay ve Anahtar kullanıldı.")
        elif self.current_village_index == 7:  # 7. köy kurtarıldıktan sonra
            print("Altın ve Kalkan kullanıldı.")

    def use_item(self):
        print("\n1. Öğe Kullan")
        print("2. Öğe Çıkar")
        choice = input("\nSeçiminiz (1-2): ")
        
        if choice == "1":
            if not self.inventory.items:
                print("\nÇanta boş!")
                return
                
            print("\nÇantanızdaki öğeler:")
            for i, item in enumerate(self.inventory.items, 1):
                print(f"{i}. {item}")
                
            item_name = input("\nKullanmak istediğiniz öğenin adını girin: ").lower()  # Küçük harfe çevir
            # Çantadaki tüm öğeleri küçük harfe çevirerek kontrol et
            found_item = next((item for item in self.inventory.items if item.name.lower() == item_name), None)
            if found_item:
                self.inventory.use_item(found_item.name)
                print(f"{found_item.name} başarıyla kullanıldı!")
            else:
                print("Öğe bulunamadı!")
                
        elif choice == "2":
            if not self.inventory.items:
                print("\nÇanta boş!")
                return
                
            print("\nÇantanızdaki öğeler:")
            for i, item in enumerate(self.inventory.items, 1):
                print(f"{i}. {item}")
                
            item_name = input("\nÇıkarmak istediğiniz öğenin adını girin: ").lower()  # Küçük harfe çevir
            # Çantadaki tüm öğeleri küçük harfe çevirerek kontrol et
            found_item = next((item for item in self.inventory.items if item.name.lower() == item_name), None)
            if found_item:
                self.inventory.use_item(found_item.name)
                print(f"{found_item.name} başarıyla çantadan çıkarıldı!")
            else:
                print("Öğe bulunamadı!")
        else:
            print("Geçersiz seçim!")

    def search_item(self):
        print("\n1. Çantada ara")
        print("2. Köylerde ara")
        choice = input("Seçiminiz (1-2): ")
        
        item_name = input("Aranacak öğenin adını girin: ").lower()  # Küçük harfe çevir
        
        if choice == "1":
            # Çantadaki tüm öğeleri küçük harfe çevirerek kontrol et
            found = any(item.name.lower() == item_name for item in self.inventory.items)
            if found:
                print(f"{item_name.capitalize()} çantada bulundu!")  # İlk harfi büyük yaparak göster
            else:
                print("Öğe çantada bulunamadı!")
        elif choice == "2":
            found_in_villages = []
            # Tüm köyleri kontrol et
            for village in self.villages:
                # Köydeki tüm öğeleri küçük harfe çevirerek kontrol et
                if any(item.name.lower() == item_name for item in village.inventory.items):
                    found_in_villages.append(village.name)
            
            if found_in_villages:
                print(f"\n{item_name.capitalize()} şu köylerde bulundu:")
                for village_name in found_in_villages:
                    print(f"- {village_name}")
            else:
                print("Öğe hiçbir köyde bulunamadı!")
        else:
            print("Geçersiz seçim!")

    def show_progress(self):
        print("\n=== İlerleme Durumu ===")
        if self.current_village_index < len(self.villages):
            print(f"Şu anki köy: {self.villages[self.current_village_index].name}")
        else:
            print("Tüm köyler kurtarıldı!")
            
        print("\nKurtarılan köyler:")
        liberated_count = 0
        for village in self.villages:
            if village.is_liberated:
                print(f"- {village.name}")
                liberated_count += 1
                
        print("\nKurtarılacak köyler:")
        remaining_count = 0
        for village in self.villages:
            if not village.is_liberated:
                print(f"- {village.name}")
                remaining_count += 1
                
        print(f"\nToplam ilerleme: {liberated_count}/{len(self.villages)} köy kurtarıldı.")

if __name__ == "__main__":
    game = Game()
    game.show_menu() 