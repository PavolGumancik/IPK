# IPK - Počítačové komunikace a sítě
## Projekt 1 

---

## Pavol Gumančík 
### login : xguman01

---

##### Popis:
První projekt očekává samostatné vypracování zadané úlohy z oblasti programování klient-server síťových aplikací. Předpokládá se použití základních knihoven a prostředků pro programování síťových soketů. 

##### Specifikace
Cílem projektu je implementace severu, který bude komunikovat protokolem HTTP a bude zajišťovat překlad doménových jmen. Pro překlad jmen bude server používat lokální resolver stanice na které běží - užijte přímo API, které poskytuje OS (například getnameinfo, getaddrinfo pro C/C++). 

##### Server podporuje dvě operace:
	GET
	POST
##### Implementace
Implementace proběhla v jazyce Python, konkretne *Python3.6*. Cílový program *ipk1.py* se skláda z 5 funkcí a to: 

##### Dsend()
Spracuje adresu, vzhodnoti jeji existenci a pošle data klientovi. Pouze pro příkaz GET

##### opGet()
Vyhodnotí szntax instrukce, získa adresu pro další postup a yavola funkci Dsend.
##### opPost()
Vyhodnotí dodatečné parametry instrukce a spracuje výstup.

##### DTload()
Funkce dekóduje data vyhodnotí správnost operace a následne předá přikaz podle ní.

##### Main()
Vyhodnotí spravnost spuštení servru, při chybě ukončí vzkonáváni programu a vzpíše chzbovou hlášku viz. "Překlad a spuštění", dále vztvoři servr a yabeypečuje jeho chod, násedně volá funkci DTload.  

##### Ošetření chyb
Mohou nastat následující chyby, které nesouvisí s výsledkem při překladu dotazů:

    Vstupní URL není správné, je jiné než /resolve či /dns-query - vrací 400 Bad Request.
    Vstupní parametry pro GET jsou nesprávné nebo chybí - vrací 400 Bad Request.
    Vstupní adresa pro GET nebyla nalezena - vrací 404 Not Found
    Formát vstupu pro POST není správný - vrací 400 Bad Request.
    Operace není podporována - je použita jiná operace než GET a POST - vrací 405 Method Not Allowed.

##### Překlad a spuštění
Spuštěni probíha pomocí makefilu a to následovne

make run ```PORT=XXXX```		

> spustí server na portu XXXX, XXXX je integer v intervalu (0,65536)

##### V prípade nevalidního portu vypíše na stderr <br/>
*"Incorect format of PORT - out of range."* - XXXX je integer, ale mimo rozsahu <br/>
*"Incorect format of PORT - invalid characters."* - XXXX neni integer <br/>
##### Testování

Pro testování je možné použít nástroj *curl*. 

Příklad příkazu pro GET operaci:

```
curl localhost:5353/resolve?name=www.fit.vutbr.cz\&type=A
```

Odpověď/výstup z je na jeden řádek:

```
www.fit.vutbr.cz:A=147.229.9.23
```

Příklad příkazu pro POST operaci:

```
curl --data-binary @queries.txt -X POST http://localhost:5353/dns-query
```

Kde soubor queries.txt obsahuje toto:

```
www.fit.vutbr.cz:A
www.google.com:A
www.seznam.cz:A
147.229.14.131:PTR
ihned.cz:A
```

odpověď/výstup z curl vzpadá takto:

```
www.fit.vutbr.cz:A=147.229.9.23
www.google.com:A=216.58.201.68
www.seznam.cz:A=77.75.74.176
147.229.14.131:PTR=dhcpz131.fit.vutbr.cz
ihned.cz:A=46.255.231.42
```




