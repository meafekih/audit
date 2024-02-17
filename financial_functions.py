import pandas as pd
import numpy as np
import plotly.graph_objects as go

def load_clean(file_path):
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    JOURNAL = pd.read_excel(file_path, sheet_name='JOURNAL')


    TAB_COM = pd.read_excel(file_path, sheet_name='TAB_COM')
    JOURNAL['CODE_COM'] = JOURNAL['CODE_COM'].astype(str)
    JOURNAL = pd.merge(JOURNAL, TAB_COM[['CODE', 'LIBELLE']], left_on='CODE_COM', right_on='CODE', how='left')
    JOURNAL.drop('CODE', axis=1, inplace=True)
    JOURNAL.rename(columns={JOURNAL.columns[-1]: 'LIBELLE_CODE_COM'}, inplace=True)

    TAB_JRN = pd.read_excel(file_path, sheet_name='TAB_JRN')
    JOURNAL = pd.merge(JOURNAL, TAB_JRN[['CODE', 'LIBELLE']], left_on='CODE_JRN', right_on='CODE', how='left')
    JOURNAL.drop('CODE', axis=1, inplace=True)
    JOURNAL.rename(columns={JOURNAL.columns[-1]: 'LIBELLE_CODE_JRN'}, inplace=True)

    TAB_BDG = pd.read_excel(file_path, sheet_name='TAB_BDG')
    JOURNAL = pd.merge(JOURNAL, TAB_BDG[['CODE', 'LIBELLE']], left_on='CODE_BDG', right_on='CODE', how='left')
    JOURNAL.drop('CODE', axis=1, inplace=True)
    JOURNAL.rename(columns={JOURNAL.columns[-1]: 'LIBELLE_CODE_BDG'}, inplace=True)

    TAB_AUX = pd.read_excel(file_path, sheet_name='TAB_AUX')
    JOURNAL = pd.merge(JOURNAL, TAB_AUX[['CODE', 'LIBELLE']], left_on='CODE_AUX', right_on='CODE', how='left')
    JOURNAL.drop('CODE', axis=1, inplace=True)
    JOURNAL.rename(columns={JOURNAL.columns[-1]: 'LIBELLE_CODE_AUX'}, inplace=True)

    columns = [ 'PIECE', 'DATE', 'REFERENCE', 'LIBELLE_x', 'CODE_COM', 'LIBELLE_CODE_COM',
                        'DEBIT', 'CREDIT','CODE_AUX','LIBELLE_CODE_AUX', 'LIBELLE_CODE_JRN', 'LIBELLE_CODE_BDG']
    JOURNAL = JOURNAL[columns]
    JOURNAL['DATE'] = pd.to_datetime(JOURNAL['DATE'], format='%Y%m%d')

    for column in columns:
        missing_info = pd.DataFrame(JOURNAL.isnull().sum(), columns=['Missing Values'])
    print(missing_info)
    JOURNAL['PIECE'] = JOURNAL['PIECE'].fillna(np.nan).astype('Int64')
    JOURNAL['PIECE'] = JOURNAL['PIECE'].astype(str)#.apply(lambda x: x + '0'*(6 - len(x)))

    return JOURNAL

def Benford(df):
    amounts = pd.concat([df['DEBIT'], df['CREDIT']])
    amounts = np.abs(amounts)
    first_digits = amounts.astype(str).str[0].astype(int)

    # Calculate the expected frequencies according to Benford's Law
    expected_frequencies = pd.Series([np.log10(1 + 1 / d) for d in range(1, 10)], index=range(1, 10))
    # Calculate the observed frequencies
    observed_frequencies = first_digits.value_counts(normalize=True).sort_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=expected_frequencies.index, y=expected_frequencies.values,
                             mode='lines+markers', name='Expected Frequencies', marker=dict(color='blue')))
    fig.add_trace(go.Bar(x=observed_frequencies.index, y=observed_frequencies.values,
                         name='Observed Frequencies', marker=dict(color='red', opacity=0.5)))
    # Update layout
    fig.update_layout(
        xaxis=dict(title='First Digit'), yaxis=dict(title='Frequency'), title="Benford's Law Analysis",
        xaxis_tickvals=list(range(1, 11)), legend=dict(x=1, y=1), bargap=0.2, plot_bgcolor='rgba(0,0,0,0)')

    return fig

def Total(df, periode):  # periode 'D', 'W', 'M'
    df['DATE'] = pd.to_datetime(df['DATE'])  # Convert 'DATE' column to datetime if not already
    df.set_index('DATE', inplace=True)
    # Group transactions by month and sum the debit and credit amounts
    monthly_totals = df.resample(periode).sum()

    # Plotly plot
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly_totals.index, y=monthly_totals['CREDIT'], name='Total Credit'))
    fig.add_trace(go.Bar(x=monthly_totals.index, y=monthly_totals['DEBIT'], name='Total Debit'))

    # Update layout
    fig.update_layout(
        title='Trend Analysis of Total Debit and Credit Amounts Over Time',
        xaxis=dict(title='Date'), yaxis=dict(title='Amount'), legend=dict(x=1, y=1),
        barmode='group', plot_bgcolor='rgba(0,0,0,0)', hovermode='x')
    return fig
