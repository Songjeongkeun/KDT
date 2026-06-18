class Contact:
    def __init__(self, name, phone, address=""):
        self.name = name
        self.phone = phone
        self.address = address

    def __repr__(self):
        return (
            f"Contact(name='{self.name}', "
            f"phone='{self.phone}', address='{self.address}')"
        )

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        name = name.strip()

        if not name:
            raise ValueError("이름은 비워둘 수 없습니다")

        self.__name = name

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        phone = phone.strip()

        if not phone:
            raise ValueError("전화번호는 비워둘 수 없습니다")

        self.__phone = phone
        
    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address.strip()
