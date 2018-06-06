
#!/usr/bin/env python3
def main():
    from yandex import Translater
    tr=Translater()
    tr.set_key('trnsl.1.1.20180513T075008Z.0977a7606fc0921a.5fa98626b8990514e07e29aa73211e45f42e934f')
    tr.set_from_lang('fa')
    tr.set_to_lang('en')
    #tr.set_text('درود')
    tr.set_text(input("enter your word!\n"))
    print(tr.translate())

if __name__ == "__main__": main()