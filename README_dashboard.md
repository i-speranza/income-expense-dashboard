Simple dashbord to monitor incomes and expenses.
UI is in italian.

First of all, create a virtual environment and install the given requirements:
```
pip install requirements.txt
```

To run the demo dashboard:
```
streamlit run dashboard.py -- --filepath ./data/rendiconto_demo.csv [--title MY_TITLE]
```

The input csv must have the following columns:
- Date: [datetime.date] date of the transation 
- Operazione: [string] main description of the transaction	
- Dettagli: [string] further transaction details	
- Tipo_transazione: [string] credit card / debit card / bank account / investment / ...	
- Categoria: [string] custom transaction categorization (e.g. donation, salary, holidays, travels, health, ...)	
- Valuta: [string] EUR / USD / ...	
- Importo: [float] transaction value (positive for incomes, negative for expenses)	
- Banca: [string] bank label if transactions come from different banks	
- Transazione_speciale: [bool] useful to flag special transaction (e.g. transfers between to bank accounts)	
- Doc_version: [string] useless, can be left empty	
- Date_Time: [datetime.datetime] date and time of the transaction. useless, can be left empty
