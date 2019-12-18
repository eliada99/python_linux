See tha all objects classes in 'objects' folder.
The creation start from 'globals' file - and the access to all objects:
    import globals
    globals.<objectName>

List of object that created in globals file:
    1. hostLinuxServer
    2. hostLinuxClient
    3. serverInterfaceEth1 = HostInterfaceEth(hostLinuxServer, "eth2") - in hardCoded should be different.
    4. serverInterfaceEth2 = HostInterfaceEth(hostLinuxServer, "eth3")
    5. clientInterfaceEth1 = HostInterfaceEth(hostLinuxClient, "eth4")
    6. clientInterfaceEth2 = HostInterfaceEth(hostLinuxClient, "eth5")
    7. serverHca = HostHca(hostLinuxServer, serverInterfaceEth1, serverInterfaceEth2)
    8. clientHca = HostHca(hostLinuxClient, clientInterfaceEth1, clientInterfaceEth2)
    9. setupObjTuple = (hostLinuxServer, hostLinuxClient, serverHca, clientHca)



############### RPyC connection ##################################
Pass to connect to hosts via RPyC.
The issue is with my ARM host - python 2.7.5 is installed but no RPyC and I cant install it.
#################################################


	Python_Scripts/Modules/ssh_module.py 
	/.autodirect/QA/eliada/qa_automation_scripts_win_vpi/Python_Scripts/SDK

	
בכל מקרה 
SDK/ זה כל הקלאסים .|
שזה מה שהכי מעניין 
OS_Manager הוא הקלאס המרכזי הוא מנהל את המערכת הפעלה הוא סינגלטון כי הוא רץ לך על המכונה הנוכחית. 
הוא מחזיק בתוכו אוס אפיאיי שהוא בהתאם למערכת הפעלה ואז כל פעולה שאתה תרצה אתה תוכל לעשות בלי לשאול איזה מערכת הפעלה יש לך על המכונה. 
או אס מנג'ר גם יכול להחזיק או אס מנג'רים של מכונות מרוחקות ואז לעשות עליהם פונקציות מרוחקות. 
זהו בתכלס בהכי קצר
אם אתה תהיה צריך להריץ טרדים תגיד לי לפני כי הרחבתי את טרד כי הוא לא יכול להחזיר תוצאה

SDK\ParallelFunctionResult.py 
הוא בטח יהיה לך שימושי למה שאתה עושה
יאללה סע

