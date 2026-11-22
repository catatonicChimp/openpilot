# MQB Revision Comparison

Generated from vendor-extract.json. DBC layout/value-table comparison only; not behavioral validation.

## ACAN

### MQB_ACAN_KMatrix_V7.08F_20111109_MH.dbc

Baseline; no earlier revision compared.

### MQB_ACAN_KMatrix_V7.08.02F_20120223_MH.dbc

- `ACC_06.ACC_Status_ACC.values`: `0 "ACC_OFF_Hauptschalter_aus" 1 "ACC_INIT" 2 "ACC_STANDBY" 3 "ACC_AKTIV_regelt" 4 "ACC_OVERRIDE" 5 "nicht_definiert" 6 "reversibler_Fehler_im_ACC_System" 7 "irreversibler_Fehler_im_ACC_System" ;` -> `0 "ACC_OFF_Hauptschalter_aus" 1 "ACC_INIT" 2 "ACC_STANDBY" 3 "ACC_AKTIV_regelt" 4 "ACC_OVERRIDE" 5 "ACC_Abschaltreaktion" 6 "reversibler_Fehler_im_ACC_System" 7 "irreversibler_Fehler_im_ACC_System" ;`

### MQB_ACAN_KMatrix_V7.09F_20120531_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.10F_20121109_MH.dbc

- `TSK_06.TSK_Hauptschalter_GRA_ACC`: `ABSENT` -> `['42', '2', '1', '+', 1.0, 0.0]`
- `TSK_06.TSK_Hauptschalter_GRA_ACC.values`: `ABSENT` -> `0 "Init" 1 "Aus" 2 "Ein" 3 "Fehler" ;`

### MQB_ACAN_KMatrix_V7.11F_20130529_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.11.01F_20130611_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.12F_20131107_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.13F_20140526_MH.dbc

- `ACC_06.ACC_nachtr_Stopp_Anf`: `ABSENT` -> `['13', '1', '1', '+', 1.0, 0.0]`
- `ACC_06.ACC_nachtr_Stopp_Anf.values`: `ABSENT` -> `0 "nicht_angefordert" 1 "angefordert" ;`

### MQB_ACAN_KMatrix_V7.14F_20141104_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.15F_20150527_MH.dbc

- `TSK_06.TSK_SRBM_Anf_ASIL`: `ABSENT` -> `['44', '3', '1', '+', 1.0, 0.0]`
- `TSK_06.TSK_SRBM_Anf_ASIL.values`: `ABSENT` -> `0 "keine_SRBM_Anforderung" 1 "SRBM_Anforderung_in_ASIL_QM" 2 "SRBM_Anforderung_in_ASIL_A" 3 "SRBM_Anforderung_in_ASIL_B" 4 "SRBM_Anforderung_in_ASIL_C" ;`

### MQB_ACAN_KMatrix_V7.16F_20151104_MH.dbc

- `ACC_06.ACC_DynErhoehung`: `ABSENT` -> `['14', '1', '1', '+', 1.0, 0.0]`
- `ACC_06.ACC_DynErhoehung.values`: `ABSENT` -> `0 "normale_Verzoegerungsdynamik" 1 "erhoehte_Verzoegerungsdynamik" ;`
- `ACC_06.ACC_Freilaufstrategie_TSK`: `ABSENT` -> `['15', '1', '1', '+', 1.0, 0.0]`
- `ACC_06.ACC_Freilaufstrategie_TSK.values`: `ABSENT` -> `0 "Freilaufstr_nicht_angefordert" 1 "Freilaufstr_angefordert" ;`

### MQB_ACAN_KMatrix_V7.17F_20160602_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.18F_20161110_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.18.01F_20161208_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.19F_20170601_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.20F_20171109_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.21F_20180531_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.22F_20190221_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.23F_20190527_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.24F_20200527_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.24.01F_20200625_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_ACAN_KMatrix_V7.25F_20210601_MH.dbc

No compared layout, message-ID, or value-table differences.

## FCAN

### MQB_FCAN_KMatrix_V7.08F_20111109_MH.dbc

Baseline; no earlier revision compared.

### MQB_FCAN_KMatrix_V7.08.02F_20120223_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.09F_20120531_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.10F_20121109_MH.dbc

- `ACC_07.ACC_Anforderung_HMS`: `ABSENT` -> `['28', '3', '1', '+', 1.0, 0.0]`
- `ACC_07.ACC_Anforderung_HMS.values`: `ABSENT` -> `0 "keine_Anforderung" 1 "halten" 2 "parken" 3 "halten_Standby" 4 "anfahren" 5 "Loesen_ueber_Rampe" ;`
- `ACC_07.ACC_Freilauf_Anf`: `ABSENT` -> `['25', '1', '1', '+', 1.0, 0.0]`
- `ACC_07.ACC_Freilauf_Anf.values`: `ABSENT` -> `0 "keine Freilauf-Anforderung" 1 "Freilauf-Anforderung" ;`
- `ACC_07.ACC_Freilauf_Info`: `ABSENT` -> `['26', '2', '1', '+', 1.0, 0.0]`
- `ACC_07.ACC_Freilauf_Info.values`: `ABSENT` -> `0 "Freilauf-Freigabe durch AT-FL" 1 "kein Übergang in Freilauf zulässig" 2 "Freilauf abwerfen" 3 "Systemfehler" ;`
- `TSK_06.TSK_Hauptschalter_GRA_ACC`: `ABSENT` -> `['42', '2', '1', '+', 1.0, 0.0]`
- `TSK_06.TSK_Hauptschalter_GRA_ACC.values`: `ABSENT` -> `0 "Init" 1 "Aus" 2 "Ein" 3 "Fehler" ;`

### MQB_FCAN_KMatrix_V7.11F_20130529_MH.dbc

- `ACC_07.ACC_Folgebeschl`: `ABSENT` -> `['32', '8', '1', '+', 0.03, -4.6]`
- `ACC_07.ACC_Folgebeschl.values`: `ABSENT` -> `254 "Neutralwert" ;`
- `ACC_07.ACC_Freilauf_Info.values`: `0 "Freilauf-Freigabe durch AT-FL" 1 "kein Übergang in Freilauf zulässig" 2 "Freilauf abwerfen" 3 "Systemfehler" ;` -> `0 "Freilauf_freigegeben" 1 "kein_Uebergang_in_Freilauf_zulaessig" 2 "Freilauf_nicht_freigegeben" 3 "Freilauf_Anforderung" ;`

### MQB_FCAN_KMatrix_V7.12F_20131107_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.13F_20140526_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.14F_20141104_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.15F_20150527_MH.dbc

- `TSK_06.TSK_SRBM_Anf_ASIL`: `ABSENT` -> `['44', '3', '1', '+', 1.0, 0.0]`
- `TSK_06.TSK_SRBM_Anf_ASIL.values`: `ABSENT` -> `0 "keine_SRBM_Anforderung" 1 "SRBM_Anforderung_in_ASIL_QM" 2 "SRBM_Anforderung_in_ASIL_A" 3 "SRBM_Anforderung_in_ASIL_B" 4 "SRBM_Anforderung_in_ASIL_C" ;`

### MQB_FCAN_KMatrix_V7.16F_20151104_MH.dbc

- `ACC_07.ACC_Boost`: `ABSENT` -> `['24', '1', '1', '+', 1.0, 0.0]`
- `ACC_07.ACC_Boost.values`: `ABSENT` -> `0 "Boost_nicht_aktiv" 1 "Boost_aktiv" ;`

### MQB_FCAN_KMatrix_V7.17F_20160602_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.18F_20161110_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.19F_20170601_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.20F_20171109_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.21F_20180531_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.22F_20190221_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.23F_20190527_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.23.01F_20190925_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.23.02F_20200221_MH.dbc

- `ACC_07.ACC_Anforderung_HMS.values`: `0 "keine_Anforderung" 1 "halten" 2 "parken" 3 "halten_Standby" 4 "anfahren" 5 "Loesen_ueber_Rampe" ;` -> `0 "keine_Anforderung" 1 "halten" 2 "parken" 3 "halten_Standby" 4 "anfahren" 5 "Loesen_ueber_Rampe" 7 "HMS_uebernehmen" ;`

### MQB_FCAN_KMatrix_V7.23.03F_20200302_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.24F_20200527_MH.dbc

No compared layout, message-ID, or value-table differences.

### MQB_FCAN_KMatrix_V7.25F_20210601_MH.dbc

- `ACC_07.ACC_TA_Kurve_Abstand`: `ABSENT` -> `['40', '6', '1', '+', 5.0, 0.0]`
- `ACC_07.ACC_TA_Kurve_Abstand.values`: `ABSENT` -> `61 "groesser_300m" 62 "Init_keine_Kurvenanpassung" ;`
- `ACC_07.ACC_TA_Kurve_vDelta`: `ABSENT` -> `['46', '4', '1', '+', 5.0, 0.0]`
- `ACC_07.ACC_TA_Kurve_vDelta.values`: `ABSENT` -> `11 "Init_keine_Kurvenanpassung" ;`

