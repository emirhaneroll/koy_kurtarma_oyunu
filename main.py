from typing import List, Optional
import sys
import os
from collections import deque

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

        if item.name.lower() < node.item.name.lower():
            node.left = self._insert(node.left, item)
        else:
            node.right = self._insert(node.right, item)

        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1

        balance = self.get_balance(node)

        # Sol Sol Durumu
        if balance > 1 and item.name.lower() < node.left.item.name.lower():
            return self.right_rotate(node)

        # Sağ Sağ Durumu
        if balance < -1 and item.name.lower() > node.right.item.name.lower():
            return self.left_rotate(node)

        # Sol Sağ Durumu
        if balance > 1 and item.name.lower() > node.left.item.name.lower():
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Sağ Sol Durumu
        if balance < -1 and item.name.lower() < node.right.item.name.lower():
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def search(self, item_name: str) -> Optional[Item]:
        return self._search(self.root, item_name)

    def _search(self, node: Node, item_name: str) -> Optional[Item]:
        if not node:
            return None

        if item_name.lower() == node.item.name.lower():
            return node.item
        elif item_name.lower() < node.item.name.lower():
            return self._search(node.left, item_name)
        else:
            return self._search(node.right, item_name)

    def delete(self, item_name: str) -> bool:
        self.root = self._delete(self.root, item_name)
        # Listeden öğeyi kaldır
        self.items = [item for item in self.items if item.name.lower() != item_name.lower()]
        return True

    def _delete(self, node: Node, item_name: str) -> Optional[Node]:
        if not node:
            return None

        if item_name.lower() < node.item.name.lower():
            node.left = self._delete(node.left, item_name)
        elif item_name.lower() > node.item.name.lower():
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

class ItemNode:
    def __init__(self, item):
        self.item = item
        self.next = None
        self.count = 1  # Aynı öğeden kaç tane var

class InventoryLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_item(self, item):
        # Eğer çanta boşsa
        if not self.head:
            self.head = ItemNode(item)
            self.size += 1
            return

        # Öğeyi alfabetik sırada ekle
        current = self.head
        prev = None
        
        # Aynı isimli öğe var mı kontrol et
        while current:
            if current.item.name == item.name:
                current.count += 1
                return
            if current.item.name > item.name:
                break
            prev = current
            current = current.next

        # Yeni öğeyi ekle
        new_node = ItemNode(item)
        if prev is None:  # Başa ekleme
            new_node.next = self.head
            self.head = new_node
        else:  # Araya veya sona ekleme
            new_node.next = current
            prev.next = new_node
        self.size += 1

    def remove_item(self, item_name):
        if not self.head:
            return False

        current = self.head
        prev = None

        while current:
            if current.item.name == item_name:
                if current.count > 1:
                    current.count -= 1
                else:
                    if prev is None:  # Baştaki öğeyi sil
                        self.head = current.next
                    else:  # Aradaki veya sondaki öğeyi sil
                        prev.next = current.next
                    self.size -= 1
                return True
            prev = current
            current = current.next
        return False

    def find_item(self, item_name):
        current = self.head
        while current:
            if current.item.name == item_name:
                return current.item
            current = current.next
        return None

    def display(self):
        current = self.head
        while current:
            if current.count > 1:
                print(f"{current.item.name} (Güç: {current.item.power}) x{current.count}")
            else:
                print(f"{current.item.name} (Güç: {current.item.power})")
            current = current.next

    def get_size(self):
        return self.size

    def get_total_power(self):
        total = 0
        current = self.head
        while current:
            total += current.item.power * current.count
            current = current.next
        return total

class Village:
    def __init__(self, name: str):
        self.name = name
        self.inventory = AVLTree()
        self.is_liberated = False

    def add_item(self, item: Item):
        self.inventory.insert(item)

    def has_item(self, item_name: str) -> bool:
        return self.inventory.search(item_name) is not None

class InventoryNode:
    def __init__(self, item):
        self.item = item
        self.next = None

class Inventory:
    def __init__(self, max_capacity: int = 10):
        self.max_capacity = max_capacity
        self.head = None
        self.size = 0
        self.bst = AVLTree()

    def push(self, item: Item) -> bool:
        if self.size >= self.max_capacity:
            return False
            
        new_node = InventoryNode(item)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            
        self.size += 1
        self.bst.insert(item)
        return True

    def pop(self, item_name: str = None) -> Optional[Item]:
        if not self.head:
            return None
            
        # Eğer item_name belirtilmişse, o öğeyi bul ve çıkar
        if item_name:
            return self.use_item(item_name)
            
        # item_name belirtilmemişse, son öğeyi çıkar
        if not self.head.next:
            item = self.head.item
            self.head = None
        else:
            current = self.head
            while current.next.next:
                current = current.next
            item = current.next.item
            current.next = None
            
        self.size -= 1
        self.bst.delete(item.name)
        return item

    def use_item(self, item_name: str) -> bool:
        if not self.head:
            return False
            
        # İlk öğeyi kontrol et
        if self.head.item.name.lower() == item_name.lower():
            item = self.head.item
            self.head = self.head.next
            self.size -= 1
            self.bst.delete(item.name)
            return True
            
        # Diğer öğeleri kontrol et
        current = self.head
        while current.next:
            if current.next.item.name.lower() == item_name.lower():
                item = current.next.item
                current.next = current.next.next
                self.size -= 1
                self.bst.delete(item.name)
                return True
            current = current.next
            
        return False

    def show_inventory(self):
        print("\n=== Çanta ===")
        if not self.head:
            print("Çanta boş!")
        else:
            # Öğeleri grupla ve sayılarını hesapla
            item_counts = {}
            current = self.head
            while current:
                if current.item.name.lower() in item_counts:
                    item_counts[current.item.name.lower()]["count"] += 1
                else:
                    item_counts[current.item.name.lower()] = {
                        "count": 1,
                        "power": current.item.power,
                        "name": current.item.name
                    }
                current = current.next
            
            # Her öğeyi ve sayısını göster
            for item_info in sorted(item_counts.values(), key=lambda x: x["name"]):
                if item_info["count"] > 1:
                    print(f"{item_info['name']} (Güç: {item_info['power']}) x{item_info['count']}")
                else:
                    print(f"{item_info['name']} (Güç: {item_info['power']})")

    def get_size(self):
        return self.size

    def get_total_power(self):
        total = 0
        current = self.head
        while current:
            total += current.item.power
            current = current.next
        return total

    def search_item(self, item_name: str) -> Optional[Item]:
        return self.bst.search(item_name)

class VillageNode:
    def __init__(self, village):
        self.village = village
        self.next = None

class VillageQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, village: Village):
        """Kuyruğa köy ekler"""
        new_node = VillageNode(village)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self) -> Optional[Village]:
        """Kuyruktan köy çıkarır"""
        if self.head is None:
            return None
        
        village = self.head.village
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return village

    def peek(self) -> Optional[Village]:
        """Kuyruğun başındaki köyü gösterir"""
        if self.head is None:
            return None
        return self.head.village

    def is_empty(self) -> bool:
        """Kuyruğun boş olup olmadığını kontrol eder"""
        return self.head is None

class Game:
    def __init__(self):
        # Köyleri oluştur
        villages = [
            Village("Yeşilvadi"),
            Village("Gümüşköy"),
            Village("Altınşehir"),
            Village("Demirtepe"),
            Village("Kristalköy"),
            Village("Zümrütvadi"),
            Village("Elmasşehir")
        ]
        
        # Köyleri bağlı listede tut
        self.villages = None
        for village in villages:
            new_node = VillageNode(village)
            if self.villages is None:
                self.villages = new_node
            else:
                current = self.villages
                while current.next:
                    current = current.next
                current.next = new_node
        
        # Kurtarma kuyruğunu oluştur
        self.liberation_queue = VillageQueue()
        # Köyleri kuyruğa ekle
        current = self.villages
        while current:
            self.liberation_queue.enqueue(current.village)
            current = current.next
        
        self.inventory = Inventory()
        self.initialize_villages()

    def get_current_village(self) -> Optional[Village]:
        """Kuyruğun başındaki köyü döndürür"""
        return self.liberation_queue.peek()

    def remove_current_village(self):
        """Kuyruğun başındaki köyü çıkarır"""
        self.liberation_queue.dequeue()

    def liberate_village(self):
        current_village = self.get_current_village()
        if not current_village:
            print("Tüm köyler kurtarıldı!")
            return

        print(f"\n{current_village.name} köyünü kurtarmaya çalışıyorsunuz...")
        
        # Köy sayısını hesapla
        total_villages = 7  # Toplam köy sayısı
        remaining_villages = self._count_villages()  # Kalan köy sayısı
        liberated_villages = total_villages - remaining_villages  # Kurtarılan köy sayısı
        
        # 5. köy için özel güç puanı sistemi (4 köy kurtarıldıktan sonra)
        if liberated_villages == 4:  # 5. köy
            required_power = 7
            total_power = 0
            
            while total_power < required_power:
                print(f"\nKristalköy köyünü kurtarmak için içerdeki casusuna en az {required_power} güç puanı vermen gerekiyor.")
                print(f"Şu ana kadar verilen güç puanı: {total_power}")
                print(f"Kalan güç puanı: {required_power - total_power}")
                
                print("\nÇantanızdaki öğeler:")
                current = self.inventory.head
                i = 1
                while current:
                    print(f"{i}. {current.item.name} (Güç: {current.item.power})")
                    current = current.next
                    i += 1
                
                item_name = input("\nKullanmak istediğiniz öğenin adını girin: ")
                found_item = self.inventory.search_item(item_name)
                if found_item:
                    if self.inventory.pop(item_name):
                        total_power += found_item.power
                        print(f"{found_item.name} kullanıldı. Güç puanı: {found_item.power}")
                        print(f"Toplam güç puanı: {total_power}")
                    else:
                        print("Öğe kullanılamadı!")
                else:
                    print("Öğe bulunamadı! Lütfen listedeki öğelerden birini seçin.")
                    continue
            
            print(f"\nToplam {total_power} güç puanı toplandı!")
            print(f"{current_village.name} köyü başarıyla kurtarıldı!")
            
            # Köydeki öğeleri çantaya ekle
            print("\nKöyden alınan öğeler:")
            for item in current_village.inventory.items:
                while True:
                    if not self.inventory.push(item):
                        print("\nÇanta dolu! Bir öğe çıkarmalısınız.")
                        print("\nÇantanızdaki öğeler:")
                        current = self.inventory.head
                        i = 1
                        while current:
                            print(f"{i}. {current.item.name} (Güç: {current.item.power})")
                            current = current.next
                            i += 1
                        item_to_remove = input("\nÇıkarmak istediğiniz öğenin adını girin: ")
                        if self.inventory.pop(item_to_remove):
                            if self.inventory.push(item):
                                print(f"{item_to_remove} çantadan çıkarıldı ve {item.name} eklendi.")
                                break
                            else:
                                print("Çanta hala dolu! Başka bir öğe çıkarmalısınız.")
                        else:
                            print("Öğe bulunamadı! Lütfen listedeki öğelerden birini seçin.")
                            continue
                    else:
                        print(f"- {item.name} (Güç: {item.power})")
                        break
            
            current_village.is_liberated = True
            self.remove_current_village()  # Kuyruktan çıkar
            return

        # 6. köy için bulmaca sistemi (5 köy kurtarıldıktan sonra)
        elif liberated_villages == 5:  # 6. köy
            print("\nKöy girişindeki kapıyı açmak için bir bulmaca var!")
            print("\nBULMACA:")
            print("Kristalköy ve Zümrütvadi köylerindeki envanterlerin baş harflerinden oluşan 4 harfli bir kelime bulun.")
            print("Bu kelimenin harfleri Kristalköy ve Zümrütvadi'de gizli.")
            print("\nİpucu: Kristalköy'deki envanterler: Altın, Zırh, Ok-Yay")
            print("İpucu: Zümrütvadi'deki envanterler: Yiyecek, Anahtar, Kılıç")
            
            while True:
                answer = input("\nBulmacanın cevabını girin (büyük harflerle): ").upper()
                if answer == "KAYA":
                    print("\nTebrikler! Bulmacayı doğru çözdünüz!")
                    print(f"{current_village.name} köyü başarıyla kurtarıldı!")
                    
                    # Köydeki öğeleri çantaya ekle
                    print("\nKöyden alınan öğeler:")
                    for item in current_village.inventory.items:
                        while True:
                            if not self.inventory.push(item):
                                print("\nÇanta dolu! Bir öğe çıkarmalısınız.")
                                print("\nÇantanızdaki öğeler:")
                                current = self.inventory.head
                                i = 1
                                while current:
                                    print(f"{i}. {current.item.name} (Güç: {current.item.power})")
                                    current = current.next
                                    i += 1
                                item_to_remove = input("\nÇıkarmak istediğiniz öğenin adını girin: ")
                                if self.inventory.pop(item_to_remove):
                                    if self.inventory.push(item):
                                        print(f"{item_to_remove} çantadan çıkarıldı ve {item.name} eklendi.")
                                        break
                                    else:
                                        print("Çanta hala dolu! Başka bir öğe çıkarmalısınız.")
                                else:
                                    print("Öğe bulunamadı! Lütfen listedeki öğelerden birini seçin.")
                                    continue
                            else:
                                print(f"- {item.name} (Güç: {item.power})")
                                break
                    
                    current_village.is_liberated = True
                    self.remove_current_village()  # Kuyruktan çıkar
                    return
                else:
                    print("Yanlış cevap! Tekrar deneyin.")
                    print("\nİpucu: Kristalköy'deki envanterler: Altın, Zırh, Ok-Yay")
                    print("İpucu: Zümrütvadi'deki envanterler: Yiyecek, Anahtar, Kılıç")

        # 7. köy için çanta yönetimi sistemi (6 köy kurtarıldıktan sonra)
        elif liberated_villages == 6:  # 7. köy
            print("\nKöyde dar bir geçit var. Bu geçidi geçmek için çantanızda en fazla 7 ürün olmalı.")
            items_to_remove = self.inventory.size - 7
            if items_to_remove > 0:
                print(f"{items_to_remove} ürün çıkarmanız gerekiyor.")
            
            while self.inventory.size > 7:
                print("\nÇantanızdaki öğeler:")
                current = self.inventory.head
                i = 1
                while current:
                    print(f"{i}. {current.item.name} (Güç: {current.item.power})")
                    current = current.next
                    i += 1
                
                try:
                    item_numbers = input("\nÇıkarmak istediğiniz ürünlerin numaralarını boşlukla ayırarak girin (1-10): ")
                    numbers = [int(num) for num in item_numbers.split()]
                    
                    # Geçerli numara kontrolü
                    if not all(1 <= num <= self.inventory.size for num in numbers):
                        print("Geçersiz numara! Lütfen listedeki numaralardan seçin.")
                        continue
                    
                    # Tekrarlanan numara kontrolü
                    if len(numbers) != len(set(numbers)):
                        print("Aynı numarayı birden fazla kez seçemezsiniz!")
                        continue
                    
                    # Seçilen ürünleri çıkar
                    current = self.inventory.head
                    i = 1
                    items_to_remove = []
                    while current:
                        if i in numbers:
                            items_to_remove.append(current.item.name)
                        current = current.next
                        i += 1
                    
                    for item_name in items_to_remove:
                        if self.inventory.pop(item_name):
                            print(f"{item_name} çantadan çıkarıldı.")
                    
                except ValueError:
                    print("Lütfen geçerli numaralar girin!")
                    continue
            
            print(f"\nÇantanızda {self.inventory.size} ürün kaldı.")
            print(f"{current_village.name} köyü başarıyla kurtarıldı!")
            
            # Köydeki öğeleri çantaya ekle
            print("\nKöyden alınan öğeler:")
            for item in current_village.inventory.items:
                while True:
                    if not self.inventory.push(item):
                        print("\nÇanta dolu! Bir öğe çıkarmalısınız.")
                        print("\nÇantanızdaki öğeler:")
                        current = self.inventory.head
                        i = 1
                        while current:
                            print(f"{i}. {current.item.name} (Güç: {current.item.power})")
                            current = current.next
                            i += 1
                        item_to_remove = input("\nÇıkarmak istediğiniz öğenin adını girin: ")
                        if self.inventory.pop(item_to_remove):
                            if self.inventory.push(item):
                                print(f"{item_to_remove} çantadan çıkarıldı ve {item.name} eklendi.")
                                break
                            else:
                                print("Çanta hala dolu! Başka bir öğe çıkarmalısınız.")
                        else:
                            print("Öğe bulunamadı! Lütfen listedeki öğelerden birini seçin.")
                            continue
                    else:
                        print(f"- {item.name} (Güç: {item.power})")
                        break
            
            current_village.is_liberated = True
            self.remove_current_village()  # Kuyruktan çıkar
            return

        # Normal köyler için
        # Köydeki öğeleri çantaya ekle
        for item in current_village.inventory.items:
            while True:
                if not self.inventory.push(item):
                    print("\nÇanta dolu! Bir öğe çıkarmalısınız.")
                    print("\nÇantanızdaki öğeler:")
                    current = self.inventory.head
                    i = 1
                    while current:
                        print(f"{i}. {current.item.name} (Güç: {current.item.power})")
                        current = current.next
                        i += 1
                    item_to_remove = input("\nÇıkarmak istediğiniz öğenin adını girin: ")
                    if self.inventory.pop(item_to_remove):
                        if self.inventory.push(item):
                            print(f"{item_to_remove} çantadan çıkarıldı ve {item.name} eklendi.")
                            break
                        else:
                            print("Çanta hala dolu! Başka bir öğe çıkarmalısınız.")
                    else:
                        print("Öğe bulunamadı! Lütfen listedeki öğelerden birini seçin.")
                    continue
                else:
                    print(f"- {item.name} (Güç: {item.power})")
                    break

        current_village.is_liberated = True
        self.remove_current_village()  # Kuyruktan çıkar
        print(f"{current_village.name} köyü başarıyla kurtarıldı!")
        print("\nKöyden alınan öğeler:")
        for item in current_village.inventory.items:
            print(f"- {item.name} (Güç: {item.power})")

    def _count_villages(self):
        """Kuyruktaki köy sayısını döndürür"""
        return self.liberation_queue.size

    def show_progress(self):
        print("\n=== İlerleme Durumu ===")
        
        # Tüm köylerin listesi
        all_villages = ["Yeşilvadi", "Gümüşköy", "Altınşehir", "Demirtepe", 
                       "Kristalköy", "Zümrütvadi", "Elmasşehir"]
        
        # Şu anki köyü göster
        current_village = self.get_current_village()
        if current_village:
            print(f"Şu anki köy: {current_village.name}")
        else:
            print("Tüm köyler kurtarıldı!")
            
        print("\nKurtarılan köyler:")
        liberated_count = 0
        for village_name in all_villages:
            # Köy bağlı listede kurtarılmış olarak işaretlenmişse
            found = False
            current = self.villages
            while current:
                if current.village.name == village_name and current.village.is_liberated:
                    found = True
                    break
                current = current.next
            if found:
                print(f"- {village_name}")
                liberated_count += 1
                
        print("\nKurtarılacak köyler:")
        remaining_count = 0
        current = self.villages
        while current:
            if not current.village.is_liberated:
                print(f"- {current.village.name}")
                remaining_count += 1
            current = current.next
                
        print(f"\nToplam ilerleme: {liberated_count}/7 köy kurtarıldı.")

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

    def show_inventory(self):
        self.inventory.show_inventory()

    def use_item(self):
        print("\n1. Öğe Kullan")
        print("2. Öğe Çıkar")
        choice = input("\nSeçiminiz (1-2): ")
        
        if choice == "1":
            if not self.inventory.head:
                print("\nÇanta boş!")
                return
                
            print("\nÇantanızdaki öğeler:")
            current = self.inventory.head
            i = 1
            while current:
                print(f"{i}. {current.item.name} (Güç: {current.item.power})")
                current = current.next
                i += 1
                
            item_name = input("\nKullanmak istediğiniz öğenin adını girin: ")
            if self.inventory.pop(item_name):
                print(f"{item_name} başarıyla kullanıldı!")
            else:
                print("Öğe bulunamadı!")
                
        elif choice == "2":
            if not self.inventory.head:
                print("\nÇanta boş!")
                return
                
            print("\nÇantanızdaki öğeler:")
            current = self.inventory.head
            i = 1
            while current:
                print(f"{i}. {current.item.name} (Güç: {current.item.power})")
                current = current.next
                i += 1
                
            item_name = input("\nÇıkarmak istediğiniz öğenin adını girin: ")
            if self.inventory.pop(item_name):
                print(f"{item_name} başarıyla çantadan çıkarıldı!")
            else:
                print("Öğe bulunamadı!")
        else:
            print("Geçersiz seçim!")

    def search_item(self):
        print("\n1. Çantada ara")
        print("2. Köylerde ara")
        choice = input("Seçiminiz (1-2): ")
        
        item_name = input("Aranacak öğenin adını girin: ")
        
        if choice == "1":
            # BST'de ara
            found_item = self.inventory.search_item(item_name)
            if found_item:
                print(f"{found_item.name} çantada bulundu!")
            else:
                print("Öğe çantada bulunamadı!")
        elif choice == "2":
            found_in_villages = []
            current = self.villages
            while current:
                # Her köyün BST'sinde ara
                if current.village.inventory.search(item_name):
                    found_in_villages.append(current.village.name)
                current = current.next
            
            if found_in_villages:
                print(f"\n{item_name} şu köylerde bulundu:")
                for village_name in found_in_villages:
                    print(f"- {village_name}")
            else:
                print("Öğe hiçbir köyde bulunamadı!")
        else:
            print("Geçersiz seçim!")

    def initialize_villages(self):
        # Tüm öğeleri tanımla
        all_items = {
            "Kılıç": Item("Kılıç", 10),
            "Büyü": Item("Büyü", 5),
            "Harita": Item("Harita", 2),
            "Balta": Item("Balta", 8),
            "Altın": Item("Altın", 15),
            "Yiyecek": Item("Yiyecek", 3),
            "Bakır": Item("Bakır", 4),
            "Gümüş": Item("Gümüş", 6),
            "Kalkan": Item("Kalkan", 7),
            "Zırh": Item("Zırh", 12),
            "Anahtar": Item("Anahtar", 1),
            "Meşale": Item("Meşale", 2),
            "Ok-Yay": Item("Ok-Yay", 9)
        }
        
        # Her köy için özel öğe kombinasyonları
        village_items = {
            "Yeşilvadi": [all_items["Kılıç"], all_items["Yiyecek"], all_items["Kalkan"]],
            "Gümüşköy": [all_items["Büyü"], all_items["Bakır"], all_items["Zırh"]],
            "Altınşehir": [all_items["Harita"], all_items["Gümüş"], all_items["Anahtar"]],
            "Demirtepe": [all_items["Balta"], all_items["Kalkan"], all_items["Meşale"]],
            "Kristalköy": [all_items["Altın"], all_items["Zırh"], all_items["Ok-Yay"]],
            "Zümrütvadi": [all_items["Yiyecek"], all_items["Anahtar"], all_items["Kılıç"]],
            "Elmasşehir": [all_items["Bakır"], all_items["Meşale"], all_items["Büyü"]]
        }
        
        # Köyleri yeniden oluştur
        current = self.villages
        while current:
            village_name = current.village.name
            # Köyün envanterini temizle
            current.village.inventory = AVLTree()
            # Köye öğeleri ekle
            for item in village_items[village_name]:
                current.village.add_item(item)
            current = current.next

    def list_villages(self):
        print("\n=== Köyler ===")
        current = self.villages
        i = 1
        while current:
            status = "Kurtarıldı" if current.village.is_liberated else "Kurtarılmadı"
            items_str = ", ".join([item.name for item in current.village.inventory.items])
            print(f"{i}. {current.village.name} - {status}")
            print(f"   Öğeler: {items_str}")
            print()
            current = current.next
            i += 1

if __name__ == "__main__":
    game = Game()
    game.show_menu() 