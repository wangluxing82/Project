import json
import os
from datetime import datetime, timedelta

DATA_FILE = "library_data.json"
REPORT_FILE = 'report.txt'


def load_data():
    """โหลดข้อมูลจากไฟล์"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"books": {}, "members": {}, "borrows": []}

def save_data(data):
    """บันทึกข้อมูลลงไฟล์"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_book(data):
    """เพิ่มหนังสือ"""
    print("\n=== เพิ่มหนังสือ ===")
    book_id = input("รหัสหนังสือ: ").strip()
    if book_id in data["books"]:
        print("รหัสหนังสือนี้มีอยู่แล้ว!")
        return
    book_name = input("ชื่อหนังสือ: ").strip()
    data["books"][book_id] = {"name": book_name, "available": True}
    save_data(data)
    print("เพิ่มหนังสือสำเร็จ!")

def delete_book(data):
    """ลบหนังสือ"""
    print("\n=== ลบหนังสือ ===")
    book_id = input("รหัสหนังสือที่จะลบ: ").strip()
    if book_id not in data["books"]:
        print("ไม่พบรหัสหนังสือนี้!")
        return
    # เช็คว่ามีการยืมอยู่หรือไม่
    for borrow in data["borrows"]:
        if book_id in borrow["book_ids"] and borrow["status"] == "ยืมอยู่":
            print("ไม่สามารถลบได้ เนื่องจากหนังสือเล่มนี้กำลังถูกยืมอยู่!")
            return
    del data["books"][book_id]
    save_data(data)
    print("ลบหนังสือสำเร็จ!")

def edit_book(data):
    """แก้ไขหนังสือ"""
    print("\n=== แก้ไขหนังสือ ===")
    old_id = input("รหัสหนังสือที่จะแก้ไข: ").strip()
    if old_id not in data["books"]:
        print("ไม่พบรหัสหนังสือนี้!")
        return
    print(f"ข้อมูลปัจจุบัน - รหัส: {old_id}, ชื่อ: {data['books'][old_id]['name']}")
    new_id = input("รหัสหนังสือใหม่ (Enter = ไม่เปลี่ยน): ").strip()
    new_name = input("ชื่อหนังสือใหม่ (Enter = ไม่เปลี่ยน): ").strip()
    
    if new_id and new_id != old_id:
        if new_id in data["books"]:
            print("รหัสหนังสือใหม่ซ้ำกับที่มีอยู่!")
            return
        data["books"][new_id] = data["books"][old_id]
        del data["books"][old_id]
        # อัพเดตในรายการยืม
        for borrow in data["borrows"]:
            if old_id in borrow["book_ids"]:
                idx = borrow["book_ids"].index(old_id)
                borrow["book_ids"][idx] = new_id
        old_id = new_id
    
    if new_name:
        data["books"][old_id]["name"] = new_name
    
    save_data(data)
    print("แก้ไขหนังสือสำเร็จ!")

def view_books(data):
    """ดูรายชื่อหนังสือ"""
    print("\n=== รายชื่อหนังสือทั้งหมด ===")
    if not data["books"]:
        print("ไม่มีหนังสือในระบบ")
        return
    print(f"{'รหัสหนังสือ':<15} {'ชื่อหนังสือ':<40} {'สถานะ':<10}")
    print("-" * 70)
    for book_id, book_info in data["books"].items():
        status = "พร้อมให้ยืม" if book_info["available"] else "ถูกยืมแล้ว"
        print(f"{book_id:<15} {book_info['name']:<40} {status:<10}")

def add_member(data):
    """เพิ่มสมาชิก"""
    print("\n=== เพิ่มสมาชิก ===")
    member_id = input("รหัสนักศึกษา: ").strip()
    if member_id in data["members"]:
        print("รหัสนักศึกษานี้มีอยู่แล้ว!")
        return
    name = input("ชื่อ: ").strip()
    phone = input("เบอร์โทร: ").strip()
    data["members"][member_id] = {"name": name, "phone": phone}
    save_data(data)
    print("เพิ่มสมาชิกสำเร็จ!")

def edit_member(data):
    """แก้ไขหรือลบสมาชิก"""
    print("\n=== แก้ไข/ลบสมาชิก ===")
    member_id = input("รหัสนักศึกษา: ").strip()
    if member_id not in data["members"]:
        print("ไม่พบรหัสนักศึกษานี้!")
        return
    
    print(f"ข้อมูลปัจจุบัน - ชื่อ: {data['members'][member_id]['name']}, เบอร์: {data['members'][member_id]['phone']}")
    print("1. แก้ไขข้อมูล")
    print("2. ลบสมาชิก")
    choice = input("เลือก (1-2): ").strip()
    
    if choice == "1":
        new_name = input("ชื่อใหม่ (Enter = ไม่เปลี่ยน): ").strip()
        new_phone = input("เบอร์โทรใหม่ (Enter = ไม่เปลี่ยน): ").strip()
        if new_name:
            data["members"][member_id]["name"] = new_name
        if new_phone:
            data["members"][member_id]["phone"] = new_phone
        save_data(data)
        print("แก้ไขสมาชิกสำเร็จ!")
    elif choice == "2":
        # เช็คว่ามีการยืมค้างอยู่หรือไม่
        for borrow in data["borrows"]:
            if borrow["member_id"] == member_id and borrow["status"] == "ยืมอยู่":
                print("ไม่สามารถลบได้ เนื่องจากสมาชิกมีหนังสือยืมค้างอยู่!")
                return
        del data["members"][member_id]
        save_data(data)
        print("ลบสมาชิกสำเร็จ!")

def view_members(data):
    """ดูรายชื่อสมาชิก"""
    print("\n=== รายชื่อสมาชิกทั้งหมด ===")
    if not data["members"]:
        print("ไม่มีสมาชิกในระบบ")
        return
    print(f"{'รหัสนักศึกษา':<15} {'ชื่อ':<30}        {'เบอร์โทร':<15}")
    print("-" * 65)
    for member_id, member_info in data["members"].items():
        print(f"{member_id:<15} {member_info['name']:<30} {member_info['phone']:<15}")

def borrow_books(data):
    """ยืมหนังสือ"""
    print("\n=== ยืมหนังสือ ===")
    member_id = input("รหัสนักศึกษา: ").strip()
    if member_id not in data["members"]:
        print("ไม่พบรหัสนักศึกษานี้!")
        return
    
    # เช็คจำนวนหนังสือที่ยืมอยู่
    current_borrows = 0
    for borrow in data["borrows"]:
        if borrow["member_id"] == member_id and borrow["status"] == "ยืมอยู่":
            current_borrows += len(borrow["book_ids"])
    
    if current_borrows >= 3:
        print("คุณยืมหนังสือครบ 3 เล่มแล้ว ไม่สามารถยืมเพิ่มได้!")
        return
    
    max_borrow = 3 - current_borrows
    print(f"คุณสามารถยืมได้อีก {max_borrow} เล่ม")
    
    num_books = int(input(f"จำนวนหนังสือที่ต้องการยืม (1-{max_borrow}): ").strip())
    if num_books < 1 or num_books > max_borrow:
        print(f"กรุณาใส่จำนวน 1-{max_borrow} เล่ม!")
        return
    
    book_ids = []
    for i in range(num_books):
        book_id = input(f"รหัสหนังสือเล่มที่ {i+1}: ").strip()
        if book_id not in data["books"]:
            print(f"ไม่พบรหัสหนังสือ {book_id}!")
            return
        if not data["books"][book_id]["available"]:
            print(f"หนังสือ {book_id} ถูกยืมไปแล้ว!")
            return
        if book_id in book_ids:
            print("ห้ามยืมหนังสือเล่มซ้ำ!")
            return
        book_ids.append(book_id)
    # บันทึกการยืม
    borrow_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    
    borrow_record = {
        "member_id": member_id,
        "book_ids": book_ids,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "return_date": None,
        "status": "ยืมอยู่"
    }
    data["borrows"].append(borrow_record)
    # อัพเดตสถานะหนังสือ
    for book_id in book_ids:
        data["books"][book_id]["available"] = False
    
    save_data(data)
    print("ยืมหนังสือสำเร็จ!")

def return_books(data):
    """คืนหนังสือ"""
    print("\n=== คืนหนังสือ ===")
    num_books = int(input("จำนวนหนังสือที่ต้องการคืน (1-3): ").strip())
    if num_books < 1 or num_books > 3:
        print("กรุณาใส่จำนวน 1-3 เล่ม!")
        return
    
    book_ids_to_return = []
    for i in range(num_books):
        book_id = input(f"รหัสหนังสือเล่มที่ {i+1}: ").strip()
        if book_id not in data["books"]:
            print(f"ไม่พบรหัสหนังสือ {book_id}!")
            return
        book_ids_to_return.append(book_id)
    
    return_date = datetime.now().strftime("%Y-%m-%d")
    returned_count = 0
    # ค้นหาและอัพเดตการยืม
    for borrow in data["borrows"]:
        if borrow["status"] == "ยืมอยู่":
            books_to_remove = []
            for book_id in book_ids_to_return:
                if book_id in borrow["book_ids"]:
                    books_to_remove.append(book_id)
                    data["books"][book_id]["available"] = True
                    returned_count += 1
            
            # ลบหนังสือที่คืนออกจากรายการ
            for book_id in books_to_remove:
                borrow["book_ids"].remove(book_id)
            
            # ถ้าคืนหมดแล้ว อัพเดตสถานะ
            if not borrow["book_ids"]:
                borrow["return_date"] = return_date
                borrow["status"] = "คืนแล้ว"
    
    save_data(data)
    if returned_count > 0:
        print(f"คืนหนังสือสำเร็จ {returned_count} เล่ม!")
        print(f"วันที่คืน: {return_date}")
    else:
        print("ไม่พบหนังสือที่ต้องการคืน หรือหนังสือไม่ได้ถูกยืมอยู่!")


def check_status(data):
    """เช็คสถานะการยืม"""
    print("\n=== สถานะการยืมหนังสือ ===")
    if not data["borrows"]:
        print("ไม่มีข้อมูลการยืม")
        return
    
    print(f"{'MemberID':<12} {'Membername':<20} {'Phone Number':<15} {'Bookname':<50} {'Borrow Date':<12} {'Due Date':<12} {'Return Date':<12} {'Status':<10}")
    print("-" * 155)
    
    for borrow in data["borrows"]:
        member_id = borrow["member_id"]
        if member_id not in data["members"]:
            continue
        
        member_name = data["members"][member_id]["name"]
        phone = data["members"][member_id]["phone"]

       # รวมชื่อหนังสือ
        book_names = []
        for book_id in borrow["book_ids"]:
            if book_id in data["books"]:
                book_names.append(data["books"][book_id]["name"])
        bookname = "\n".join(book_names) if book_names else "-"     
                
        borrow_date = borrow["borrow_date"]
        due_date = borrow["due_date"]
        return_date = borrow["return_date"] if borrow["return_date"] else "-"
        status = borrow["status"]
        
        print(f"{member_id:<12} {member_name:<20} {phone:<15} {bookname:<50} {borrow_date:<12} {due_date:<12} {return_date:<12} {status:<10}")

    

def build_report_text(data):
    """สร้างรายงานแบบสวยงามตามต้นแบบ"""
    lines = []
    now = datetime.now()
    
    # ส่วนหัว
    lines.append("Library Borrow System - Summary Report")
    lines.append(f"Generated At : {now.strftime('%Y-%m-%d %H:%M:%S')} (+0700)")
    lines.append("App Version  : 2.0")
    lines.append("Encoding     : UTF-8 (fixed-length)")
    lines.append("")
    lines.append("-" * 160)
    
    # หัวตาราง
    lines.append(f"{'MemberID':<10} | {'Membername':<25} | {'Phone Number':<15} | {'Bookname':<40} | {'Borrow Date':<13} | {'Due Date':<13} | {'Return Date':<13} | {'Status':<10}")
    lines.append("-" * 160)
    
    # แสดงข้อมูลการยืม
    if data["borrows"]:
        for borrow in data["borrows"]:
            member_id = borrow["member_id"]
            if member_id not in data["members"]:
                continue
            
            member_name = data["members"][member_id]["name"][:23]
            phone = data["members"][member_id]["phone"]
            borrow_date = borrow["borrow_date"]
            due_date = borrow["due_date"]
            return_date = borrow["return_date"] if borrow["return_date"] else "-"
            status = borrow["status"]
            
            # รวมชื่อหนังสือ
            book_names = []
            for book_id in borrow["book_ids"]:
                if book_id in data["books"]:
                    book_names.append(data["books"][book_id]["name"])
            
            # แสดงหนังสือ
            if book_names:
                for idx, book_name in enumerate(book_names):
                    book_display = f"{idx+1}.{book_name[:37]}"
                    if idx == 0:
                        lines.append(f"{member_id:<10} | {member_name:<25} | {phone:<15} | {book_display:<40} | {borrow_date:<13} | {due_date:<13} | {return_date:<13} | {status:<10}")
                    else:
                        lines.append(f"{'':>10} | {'':>25} | {'':>15} | {book_display:<40} | {'':>13} | {'':>13} | {'':>13} | {'':>10}")
            else:
                lines.append(f"{member_id:<10} | {member_name:<25} | {phone:<15} | {'-':<40} | {borrow_date:<13} | {due_date:<13} | {return_date:<13} | {status:<10}")
    else:
        lines.append("No borrow records".center(160))
    
    lines.append("-" * 160)
    lines.append("")
    
    # สรุปข้อมูล
    total_books = len(data["books"])
    active_books = total_books
    deleted_books = 0
    borrowed_now = sum(1 for b in data["books"].values() if not b.get("available", True))
    available_now = total_books - borrowed_now
    
    lines.append("Summary (Active Books Only)")
    lines.append(f"- Total Books    : {total_books}")
    lines.append(f"- Active Books   : {active_books}")
    lines.append(f"- Deleted Books  : {deleted_books}")
    lines.append(f"- Borrowed Now   : {borrowed_now}")
    lines.append(f"- Available Now  : {available_now}")
    lines.append("")
    
    # สถิติการยืม
    if data["borrows"]:
        # หาหนังสือที่ถูกยืมบ่อยที่สุด
        book_borrow_count = {}
        for borrow in data["borrows"]:
            for book_id in borrow["book_ids"]:
                if book_id in data["books"]:
                    book_name = data["books"][book_id]["name"]
                    book_borrow_count[book_name] = book_borrow_count.get(book_name, 0) + 1
        
        if book_borrow_count:
            most_borrowed = max(book_borrow_count.items(), key=lambda x: x[1])
            lines.append("Borrow Statistics (Active only)")
            lines.append(f"- Most Borrowed Book : {most_borrowed[0]} ({most_borrowed[1]} times)")
        
        # จำนวนผู้ยืมปัจจุบัน
        active_borrowers = set()
        for borrow in data["borrows"]:
            if borrow["status"] == "ยืมอยู่":
                active_borrowers.add(borrow["member_id"])
        
        currently_borrowed_count = sum(1 for b in data["borrows"] if b["status"] == "ยืมอยู่")
        lines.append(f"- Currently Borrowed : {currently_borrowed_count}")
        lines.append(f"- Active Members     : {len(active_borrowers)}")
    
    return "\n".join(lines)
def log_action(msg):
    """บันทึก action ลงไฟล์เล็กๆ (append)"""
    try:
        with open('actions.log', 'a', encoding='utf-8') as lf:
            lf.write(f"{datetime.now().isoformat()} {msg}\n")
    except Exception:
        pass

def main():
    """ฟังก์ชันหลัก"""
    data = load_data()
    
    while True:
        print("\n" + "="*50)
        print("ระบบยืมคืนหนังสือห้องสมุด")
        print("="*50)
        print("1. เพิ่มหนังสือ")
        print("2. ลบหนังสือ")
        print("3. แก้ไขหนังสือ")
        print("4. ดูรายชื่อหนังสือ")
        print("5. เพิ่มสมาชิก")
        print("6. แก้ไขสมาชิก")
        print("7. ดูรายชื่อสมาชิก")
        print("8. ยืมหนังสือ")
        print("9. คืนหนังสือ")
        print("10. เช็คสถานะ")
        print("11.  Report")
        print("12. ออกจากระบบ")
        print("="*50)
        
        choice = input("เลือกเมนู (1-12): ").strip()
        
        if choice == "1":
            add_book(data)
        elif choice == "2":
            delete_book(data)
        elif choice == "3":
            edit_book(data)
        elif choice == "4":
            view_books(data)
        elif choice == "5":
            add_member(data)
        elif choice == "6":
            edit_member(data)
        elif choice == "7":
            view_members(data)
        elif choice == "8":
            borrow_books(data)
        elif choice == "9":
            return_books(data)
        elif choice == "10":
            check_status(data)
        elif choice == '11':
            report_text = build_report_text(data)
            with open(REPORT_FILE, 'w', encoding='utf-8') as rf:
                rf.write(report_text)
            log_action(f"Report written: {REPORT_FILE}")
            print(f"Report saved to {REPORT_FILE}")
        
        elif choice == "12":
            print("\nออกจากระบบ... ขอบคุณที่ใช้บริการ!")
            break
        else:
            print("กรุณาเลือกเมนู 1-12 เท่านั้น!")
if __name__ == "__main__":
    main()