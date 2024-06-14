from emur import EMUR_generator

if __name__ == "__main__":
    generator = EMUR_generator("data/2023.xml", "XML", 1)
    generator.run()