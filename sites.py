def linkedin(page):

    page.goto("https://www.linkedin.com/")
    
    while (1):
        cmd = input("[linkedin] --> ")
        if cmd == 'exit':
            break
        if cmd == 'dump':
            print(page.content())
        