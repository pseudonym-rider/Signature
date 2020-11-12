1. Key Server가 방역당국에게 키 전송 (Key Server -> 방역당국)<br/><br/>

    * parameters <br/>

        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |MSK-user|User's Manager Secret Key|Int|
        |MSK-owner|Owner's Manager Secret Key|Int|
        |GPK-user|User's Group Public Key|Int|
        |GPK-owner|Owner's Group Public Key|Int|
    <br/>

    * MSK-user<br/>

        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |ξ1|Element of Manager Key|Int|
        |ξ2|Element of Manager Key|Int|
    <br/>

    * MSK-owner<br/>
  
        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |ξ1|Element of Manager Key|Int|
        |ξ2|Element of Manager Key|Int|    
    <br/>

    * GPK-user<br/>
  
        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |g1| \<g1> = G1 |Int|
        |g2| \<g2> = G2 |Int|
        |h|h such that uξ1 = vξ2 = h|Int|
        |u|u, v such that uξ1 = vξ2 = h|Int|
        |v|u, v such that uξ1 = vξ2 = h|Int|
        |w| w = g2γ |Int|
    <br/>

    * GPK-owner<br/>
  
        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |g1| \<g1> = G1 |Int|
        |g2| \<g2> = G2 |Int|
        |h|h such that uξ1 = vξ2 = h|Int|
        |u|u, v such that uξ1 = vξ2 = h|Int|
        |v|u, v such that uξ1 = vξ2 = h|Int|
        |w| w = g2γ |Int|
    <br/>
2. 방문자가 token으로 그룹 개인키 발급 요청 (방문자 -> Key Server)<br/><br/>
   - Response
3. 수집서버가 token으로 그룹 개인키 발급을 요청한 방문자의 신원을 검증 (수집서버 -> Key Server)<br/><br/>
   - Response
4. 점주가 token으로 그룹 개인키 발급 요청 (점주 -> Key Server)<br/><br/>
   - Response
5. 수집서버가 token으로 그룹 개인키 발급을 요청한 점주의 신원을 검증 (수집서버 -> Key Server)<br/><br/>
   - Response

6. Key Server가 수집서버에게 그룹 공개키 전송 (Key Server -> 수집서버)<br/><br/>

    * parameters <br/>

        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |GPK-user|User's Group Public Key|Int|
        |GPK-owner|Owner's Group Public Key|Int|
    <br/>

    * GPK-user<br/>
  
        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |g1| \<g1> = G1 |Int|
        |g2| \<g2> = G2 |Int|
        |h|h such that uξ1 = vξ2 = h|Int|
        |u|u, v such that uξ1 = vξ2 = h|Int|
        |v|u, v such that uξ1 = vξ2 = h|Int|
        |w| w = g2γ |Int|
    <br/>

    * GPK-owner<br/>
  
        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |g1| \<g1> = G1 |Int|
        |g2| \<g2> = G2 |Int|
        |h|h such that uξ1 = vξ2 = h|Int|
        |u|u, v such that uξ1 = vξ2 = h|Int|
        |v|u, v such that uξ1 = vξ2 = h|Int|
        |w| w = g2γ |Int|
    <br/>