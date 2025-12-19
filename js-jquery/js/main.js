console.log('js 연결 확인')

// dom - html 전체 구조를 객체화 한것.
$(document).ready(
    function(){
        console.log('jquery 연결 확인 완료');
        $("#btn").click(function(){
            $("#text").text("버튼이 클릭되었습니다.");
        }
    )
    // 전체선택
    $("#checkall").on("change",function(){
        $('.chk').prop("checked", $(this).prop("checked")); //.prop('checked',this.checked)
    })
    }
    
);
