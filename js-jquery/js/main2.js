console.log('js 연결확인')

//  dom - html전체 구조를 객체화 한것
$(document).ready(
    function(){
        // 초기 랜더링 리스트업(READ)
        let users = [
            {id:1, name:'홍길동',email:'hong@test.com'},
            {id:2, name:'김철수',email:'kim@test.com'},
        ]
        // for user in users:
            // user     
        users.forEach(user => {
            $('#userTable').append(
                `
                <tr data-id="${user.id}">
                    <td><input type="checkbox" class="chk"></td>
                    <td>${user.id}</td>
                    <td>${user.name}</td>
                    <td>${user.email}</td>
                    <td>
                        <button class="edit">MODIFY</button>
                        <button class="remove">REMOVE</button>
                    </td>
                </tr>
                `            )
        });
        // 전체 선택 해제
        $("#checkall").on('change',function(){
            $(".chk").prop('checked',this.checked)            
        });
        // 동적생성한 요소는 이벤트위임으로 부모에게 이벤트를 위임해서 처리
        $("#userTable").on('change', '.chk', function(){            
            $("#checkall").prop('checked', 
                $(".chk").length == $(".chk:checked").length
            )
        });
        // CREATE 행 추가 - prompt
        $("#addBtn").on('click',function(){
            const name = prompt('이름 입력');
            const email = prompt('이메일 입력');
            if(!name || !email) return ;
            const newId=users[users.length-1].id+1; //javascript or java or c++ or c 스타일
            check = age >= 19? '성인':'미성년자'; // 3항 연산자
            // users[users.length-1].id+1 if user.length else 1 // python 스타일
            // if(users.length){
            //     const newId = users[users.length-1].id+1
            // }
            // else{
            //     const newId = 1
            // }
        })
    }   
);