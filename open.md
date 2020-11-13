1. 방역당국이 Key Server에게 GML(Group Member List)을 질의(방역당국 -> Key Server)  

    * parameters <br/>

        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |-|-|-|
    <br/>

    * Response <br/>

      * Success  
        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |GML|Group Member List|array|  

      * Fail 

2. 방역당국이 수집서버의 User Table에 '확진자가 다녀간 점포'정보를 질의(방역당국 -> 수집서버)<br/><br/>
   
   * parameters <br/>

        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |userName|User's Name|String|
        |userPhone|User's Phone|String|
    <br/>

    * Response <br/>


      * Success 

        * parameters
            |params|explanation|type|
            |:------:|:-------------:|:---:|
            |arrSigOwner|Array of $Sig_{owner}$s |array|
            |arrMsg|Array of $QR_{user}$s |array|
        <br/>
             
        * note that $Sig_{owner}$ = $E_{USK_{owner}}(QR_{user})$  

      * Fail 

3. 방역당국이 수집서버의 Owner Table에 '확진자가 다녀간 점포에 방문한 방문자목록'정보를 질의(방역당국 -> 수집서버)<br/><br/>
   
   * parameters <br/>

        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |arrA|Array of $A$s|array|
    <br/>

    * Response <br/>


      * Success 

        * parameters
            |params|explanation|type|
            |:------:|:-------------:|:---:|
            |arrSigOwner|Array of $Sig_{user}$s |array|
            |arrQR|Array of $(r, qrTime)$s |array|
        <br/>
             
        * note that $Sig_{user}$ = $E_{USK_{user}}(r, qrTime)$  

      * Fail 
