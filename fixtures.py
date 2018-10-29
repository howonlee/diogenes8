import dio

peep = dio.Person(email="bob@dobbs.com", name="Bob Dobbs")

email = dio.Email(
            dest_addr="howon@lee.com",
            subject="Diogenes stuff",
            text="Bob Dobbs lives again")

settings = dio.Settings(
            mailgun_domain="bobdobbs",
            mailgun_api_key="invalid")

schedule = dio.DefaultSchedule()


if __name__ == "__main__":
    raise NotImplementedError("Import this module to import the fixtures")
