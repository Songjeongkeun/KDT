from contact import Contact
from contacts_dao import ContactsDAO


class ContactsService:
    def __init__(self):
        self.dao = ContactsDAO()

    @staticmethod
    def print_contact(contact):
        address = contact["address"] or "-"
        print(
            f"이름: {contact['name']}, "
            f"전화번호: {contact['phone']}, "
            f"주소: {address}"
        )

    def insert_contact(self):
        name = input("이름을 입력하세요: ")
        phone = input("전화번호를 입력하세요: ")
        address = input("주소를 입력하세요(생략 가능): ")

        contact = Contact(name, phone, address)
        self.dao.insert(contact)
        print("연락처가 등록되었습니다")

    def print_all(self):
        contacts = self.dao.select_all()

        if not contacts:
            print("등록된 연락처가 없습니다")
            return

        for contact in contacts:
            self.print_contact(contact)

    def search_contacts(self):
        keyword = input("검색할 이름 또는 전화번호를 입력하세요: ").strip()
        contacts = self.dao.search_all(keyword)

        if not contacts:
            print("찾는 연락처가 없습니다")
            return

        for contact in contacts:
            self.print_contact(contact)

    def edit_contact(self):
        old_phone = input("수정할 연락처의 전화번호를 입력하세요: ").strip()
        saved_contact = self.dao.search(old_phone)

        if not saved_contact:
            print("수정할 연락처가 없습니다")
            return

        print("새 값을 입력하세요. 입력하지 않으면 기존 값을 유지합니다.")
        name = input(f"이름({saved_contact['name']}): ").strip()
        phone = input(f"전화번호({saved_contact['phone']}): ").strip()
        address = input(f"주소({saved_contact['address'] or '-'}): ").strip()

        contact = Contact(
            name or saved_contact["name"],
            phone or saved_contact["phone"],
            address or saved_contact["address"] or "",
        )
        result = self.dao.update(contact, old_phone)

        if result > 0:
            print("연락처가 수정되었습니다")
        else:
            print("연락처 수정에 실패했습니다")

    def delete_contact(self):
        phone = input("삭제할 연락처의 전화번호를 입력하세요: ").strip()
        contact = self.dao.search(phone)

        if not contact:
            print("삭제할 연락처가 없습니다")
            return

        result = self.dao.delete(phone)

        if result > 0:
            print("연락처가 삭제되었습니다")
        else:
            print("연락처 삭제에 실패했습니다")
