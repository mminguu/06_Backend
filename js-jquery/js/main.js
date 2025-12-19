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
    }
);
