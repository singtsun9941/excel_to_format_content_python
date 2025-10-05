class Staff:
    def __init__(self, name, staffNo, tel, schedule):
        # Instance attributes
        self.name = name
        self.staffNo = staffNo
        self.tel = tel
        self.schedule = schedule

    def __repr__(self):
        return f"Staff(name={self.name!r}, staffNo={self.staffNo!r})"
