console.log('js 연결 확인')

// dom - html 전체 구조를 객체화 한것.
$(document).ready(
    function(){
        console.log('jquery 연결 확인 완료');
        $("#btn").click(function(){
            $("#text").text("버튼이 클릭되었습니다.");
        })
        // 전체선택
        $("#checkall").on("change",function(){
            $('.chk').prop('checked',this.checked);
        });
        // 개별체크로 전체 컨트롤
        $('.chk').on('change',function(){
            const total = $('.chk').length
            const checked = $('.chk:checked').length
            $('#checkall').prop('checked',total==checked)
            // 개수를 카운트
            $('#count').text(checked)
        });
        // 선택 삭제
        $('#deleteBtn').click(function(){
            $('.tchk:checked').each(function(){
                $(this).closest('tr').remove();
            });
        });
        // 버튼 비활성화(중복 클릭 방지)  저장 결제 api 호출
        $('#saveBtn').click(function(){
            $(this).prop('disabled',true) // 버튼 활성화
        setTimeout( ()=>{
            $(this).prop('disabled',false) // 버튼 비활성화
        },2000);
        });
        // 실시간 입력값을 검증
        // $('#username').on('input',function(){
        //     const val = $(this).val()
        //     if(val.length < 3){
        //         $('#msg').text('3자 이상 입력').css('color','red')
        //     }else{
        //         $('#msg').text('사용가능').css('color','green')
        //     }
        // });
        $('#username').on('input', (e)=>{ // 화살표 함수는 this를 바인딩하지 않고 window객체를 반환
            const val=e.target.value
            if(val.length < 3){
                $('#msg').text('3자 이상 입력').css('color','red')
            }else{
                $('#msg').text('사용가능').css('color','green')
            }});
            // 동적 요소 추가
        let cnt = 1;
        $('#addBtn').click(function(){
            $('#list').append(
                `
                <div class="item">
                    동적항목 ${cnt++}
                    <span class="remove">삭제</span>
                </div>
                `
            );
        })
// 이벤트 위임
// 이벤트 위임은 on 메소드로 사용
// 부모요소.on(이벤트종류, 자식요소선택자,실행함수)
// 이유는 javascript로 동적으로 생성한 element는 javascript에서 해당요소의 이벤트를 감지못함 왜냐면
// javascript보다 나중에 생성된 element 이기때문에
// html5는 이벤트 버블링이 있어서 모든 이벤트는 부로로 전파된다는 속성을 이용해서 역으로
// 해당 부모가 이벤트를 감지해서 발생하면 자식의 바로 부모엘리먼트를 제거할수 있다
// 이것이 바로 이벤트 위임
// 테이블 , 리스트, 댓글
        $('#list').on('click', '.remove',function(){
            $(this).parent().remove();
        })
    }
);
