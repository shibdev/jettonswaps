TOKEN = 'YOUR_BOT_API_KEY_HERE'
CHAT_ID = 0

# JETTON ADDRESS
addresses = [
"EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE",
"EQC-A0ZHiAliPJ6LYQQZ6x2WRJC0aHEmJ_OMG6pidb5ASpIY",
"EQCW5g1evnQN2OZZEVe-23aSvEsgPauWZlF27ZIz5REhnWRy",
"EQD0vdSA_NedR9uvbgN9EikRX-suesDxGeFg69XQMavfLqIw",
"EQBCFwW8uFUh-amdRmNY9NyeDEaeDYXd9ggJGsicpqVcHq7B",
"EQACGPrFHWCy9QmeFXPqvZflyoeBb5grVQxAaucF0hNd1sEs",
"EQAvvEdq4x5K6owjsMI4X6AxKkTBXVKIVkiSHDLt6i2LFnnQ",
"EQBl3gg6AAdjgjO2ZoNU5Q5EzUIl8XMNZrix8Z5dJmkHUfxI",
"EQBj7uoIVsngmS-ayOz1nHENjZkjTt5mXB4uGa83hmcqq2wA",
"EQC-tdRjjoYMz3MXKW4pj95bNZgvRyWwZ23Jix3ph7guvHxJ",
"EQCcLAW537KnRg_aSPrnQJoyYjOZkzqYp6FVmRUvN1crSazV",
"EQAE8sAbvxMoIrN2tAuOe4vI5H4JhnHI-zn2VoRy-agH7BCn",
"EQB-ajMyi5-WKIgOHnbOGApfckUGbl6tDk3Qt8PKmb-xLAvp",
"EQCPmOnkTe8qP_ZtCf3Rys04ukRTiQc_xVS-lGQ6BH3JZWmC",
"EQBiJ8dSbp3_YAb_KuC64zCrFqQTsFbUee5tbzr5el_HEDGE",
"EQAYBDuLdLrjDKR1SUZ60ZuLuSzHDIoE26zZExuB_bjiG0Zr",
"EQBlHnYC0Uk13_WBK4PN-qjB2TiiXixYDTe7EjX17-IV-0eF",
"EQD0nt2W1YwJFdMQ-GIx4jguNbvbjS-aM32jOW7hTQs58lds",
"EQBk0iOnG6u4yVzf4HfZf7EGuetWiKbyR5GApBgblmeG-jPL",
"EQBjEw-SOe8yV2kIbGVZGrsPpLTaaoAOE87CGXI2ca4XdzXA",
"EQAKs_G-uCCwKNjMTRMNVau__QIAdWt02D7xkH5v1P0TO13D",
"EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA",
"EQBzyesZ3p1WGNrggNSJi6JFK3vr0GhqJp4gxker9oujjcuv",
"EQB-MPwrd1G6WKNkLz_VnV6WqBDd142KMQv-g1O-8QUA3728",
"EQDcBkGHmC4pTf34x3Gm05XvepO5w60DNxZ-XT4I6-UGG5L5",
"EQDpdmk9DyD8J1w8cZV5R411Ki38t3n-wjXrkIBD_-GDZ89a",
"EQAS2elYb6_hqWyOl7gpuYTzf1sqmjLJQ0lQ4X_4d_MvtMWR",
"EQAmixWvMs3jQaWhrvACOsVcyj4RsdLxihXtjmFMBdC9alH2",
"EQAQXlWJvGbbFfE8F3oS8s87lIgdovS455IsWFaRdmJetTon",
"EQDqQscohYilSqWEyeLyCReOQKOh7KhRX_CPlD-Qdx02tUbG",
"EQD_KpO2-iFeHPT4dF0ur9E0iAFts2fwhpR2KjwAmYKpccvH",
"EQCu9qafFYH1tbvBCsVg6QQwPbLinzQ27HKkr0Tb4WSobXI-",
"EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA",
"EQB-MPwrd1G6WKNkLz_VnV6WqBDd142KMQv-g1O-8QUA3728",
"EQDcBkGHmC4pTf34x3Gm05XvepO5w60DNxZ-XT4I6-UGG5L5",
]

# SYMBOL: LP ADDRESS
token = {
"scale": "EQDcm06RlreuMurm-yik9WbL6kI617B77OrSRF_ZjoCYFuny",
"exc": "EQD-rHe9UGVhcTF6SIEM72trdffF_pP_okSw3MCfd6Dd9wBq",
"ddao": "EQBWYs6w5lpJ15_PMh3bcTupMrGZHKXQe6ZhCOoOXzAHTglh",
"marga": "EQCHQo7Y6CP1IF4Q3fWf2k2blMLJodBO8YjeAFybgzTxyvlJ",
"redx": "EQBNtHHaL3D4PKSSc1HyTm5aIL8KUbRvIlXc2AGu1vNMC1EF",
"ivs": "EQCCM60Gove-KAwW9TqPUB6vjGfBCNk8JTAko7yoxZWPNfdd",
"kingy": "EQDsIxN6kTHNTzkW-KDAFoOd7uK8IV_qhw8wR5NkYH1Gh_SQ",
"tnx": "EQAycFS0Mr1ZsydnS6OmswoJZCDSxIciAHZFVKOrDll3FBpL",
"bolt": "EQABHkxndSnqrBgMIDR73LB0FBDDM0C_Up39EL1Rn3ao_54-",
"ggt": "EQBTQ9OLKaY2L9jsSqyyGZoZuCv6Q0_3dr7PDEBgeWZcNFIA",
"dhd": "EQAuoxgiHoLGBxLQ0lkOgpLwneX_CjroB8H8s3h1QMNLWhIW",
"jbct": "EQA3tl3ID_1C69ECyHTDYJEDUWvQwuj4WdOs5lbFGWqtFUHn",
"lave": "EQCCPQrYpU85L23q9RaEfzkXn4buefvm9KA2MhpjA8mVgcDX",
"grbs": "EQCqH726RKRhR4HG8TtUR8_ebxo0zB3D-pLdYEPHqwnvQy__",
"ambr": "EQAv6X80FaAqBSuZDAPs5uia98M14Pw5LW2MwGkj8I9TFrDb",
"kiss": "EQC1bSn8Xm5m2JNQVADGDkDa9ox8Jv6vMc0jEvapuuScnMsG",
"tnr": "EQCR_4x99hcPWXDsJHGm52IMgTOQd7Mrta1GlEruJZuOjb5u",
"hedge": "EQBqIBQDyv352Rb7pyJGBLVb4xFIyeJssy2ll-LbwZnTTQxz",
"click": "EQBm9WZCRQFPXMNQ3u8B4N8Qu2PjMtmCePUqWi4CyIaxz5Ra",
"inc": "EQCe7i11lU-VDartvgu5QEu5cNHxd9Ev0PZ1OXKn5gvmHdff",
'take': "EQCDI9YtLpHcqWc9WK6Jsne6LhKCsyIUPeUWMO4f_zU6nLUO",
'sibt': "EQDjAT0mJwzdcnycveZ-mKNAAEKMIZw1s2WFttYtC23EyCkK",
'love': "EQAeOyDl0k4gJ1DHNO8S58QTfUfswthRilI37CE-A5be2pUM",
'heh': "EQCIFoBW0L4z5BRCzH0MiQsUi_3z34J-JXWWnrOfp4uPpvqS",
'jetton': "EQD0F_w35CTWUxTWRjefoV-400KRA2jX51X4ezIgmUUY_0Qn",
'vc': "EQCV6WH5QykmB6Qg36g8h9M47o_HO9hkJHI75dkY_4m-ROM3",
'lifeyt': "EQDTYulHsoUoninbQBzLBcBhtwkXfY6Iex14bhAH6EQ978BK",
'monk': "EQAzz4E9I4n5bzmgyaNX3GObPdRw_GkmD6IZqsIs_ZlvSSiR",
'jusdt': "EQCk6tGPlFoQ_1TgZJjuiulfSJz5aoJgnyy29eLsXtOmeYDw",
'jusdc': "EQDUapdxxYjBzyR1Tw1I5QR4v2Eagdy6n2d9TcmAPbntWEmm",
'jwbtc': "EQAdyJF9ZyU66XzCepZT6Dtt7RBFzxP7rBimRf8FN62Xbw6G",
}

flipped_token = {}
for value, key in zip(token, addresses):
    flipped_token[key] = value

known_wallets = {
    "UQBMubUg_eg35keX91BElNjcy5e8p23Uj3SOEyv0tipNdOcz": "#ArbitrageBot1",
    "UQDqkETmtHJYDmZXcNTMw5KzOjMss5sFxD5vNA1XlBwk76Rt": "#ArbitrageBot2",
    "UQBinNJaqRaea7WA2oFpx5kD6tHiegj31x6UrVekkSdc2lME": "#ArbitrageBot3",
}
