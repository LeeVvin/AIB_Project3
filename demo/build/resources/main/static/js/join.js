$(document).ready(function () {
  var idx = true;
  $("#userError").hide();
  $("#emailError2").hide();
  $("#birthError").hide();
  $("#phoneError").hide();
  $("#genderError").hide();
  $("#addError").hide();
  $("#eduError").hide();
  $("#mbtiError").hide();
  $("#statusError").hide();
  $("#univError").hide();
  $("#deError").hide();
  const userClass = document.getElementById("username").classList;
  const emailClass = document.getElementById("email").classList;
  const birthClass = document.getElementById("birth").classList;
  const phoneClass = document.getElementById("phone").classList;
  const genderClass = document.getElementById("gender").classList;
  const addClass = document.getElementById("address").classList;
  const eduClass = document.getElementById("education").classList;
  const mbtiClass = document.getElementById("mbti").classList;
  const stClass = document.getElementById("status").classList;
  const univClass = document.getElementById("university").classList;
  const deClass = document.getElementById("department").classList;

  $("#submit").click(function () {
    $("#username").change(function () {
      userClass.remove("active");
      $("#userError").hide();
    });
    if ($("#username").val().length == 0) {
      $("#username").focus();
      $("#userError").show();
      userClass.add("active");
      idx = false;
    }

    if ($("#email").val().length == 0) {
      $("#email").focus();
      $("#emailError2").show();
      emailClass.add("active");
      idx = false;
    }

    $("#birth").change(function () {
      birthClass.remove("active");
      $("#birthError").hide();
    });
    if ($("#birth").val().length == 0) {
      $("#birthError").show();
      $("#birth").focus();
      birthClass.add("active");
      idx = false;
    }

    $("#phone").change(function () {
      phoneClass.remove("active");
      $("#phoneError").hide();
    });
    if ($("#phone").val().length == 0) {
      phoneClass.add("active");
      $("#phoneError").show();
      $("#phone").focus();
      idx = false;
    }

    $("select[name=gender]").change(function () {
      genderClass.remove("active");
      $("#genderError").hide();
    });
    if (!$("select[name=gender]").val()) {
      genderClass.add("active");
      $("#genderError").show();
      $("select[name=gender]").focus();
      idx = false;
    }

    $("select[name=address]").change(function () {
      addClass.remove("active");
      $("#addError").hide();
    });
    if (!$("select[name=address]").val()) {
      addClass.add("active");
      $("#addError").show();
      $("select[name=address]").focus();
      idx = false;
    }

    $("select[name=education]").change(function () {
      eduClass.remove("active");
      $("#eduError").hide();
    });
    if (!$("select[name=education]").val()) {
      eduClass.add("active");
      $("#eduError").show();
      $("select[name=education]").focus();
      idx = false;
    }
    if ($("select[name=education]").val() == "univ") {
      $("select[name=status]").change(function () {
        stClass.remove("active");
        $("#statusError").hide();
      });
      if (!$("select[name=status]").val()) {
        stClass.add("active");
        $("#statusError").show();
        $("select[name=status]").focus();
        idx = false;
      }

      $("#university").change(function () {
        univClass.remove("active");
        $("#univError").hide();
      });
      if ($("#university").val().length == 0) {
        univClass.add("active");
        $("#univError").show();
        $("#university").focus();
        idx = false;
      }

      $("#department").change(function () {
        deClass.remove("active");
        $("#deError").hide();
      });
      if ($("#department").val().length == 0) {
        deClass.add("active");
        $("#deError").show();
        $("#department").focus();
        idx = false;
      }
    }

    $("select[name=mbti]").change(function () {
      mbtiClass.remove("active");
      $("#mbtiError").hide();
    });
    if (!$("select[name=mbti]").val()) {
      mbtiClass.add("active");
      $("#mbtiError").show();
      $("select[name=mbti]").focus();
      idx = false;
    }
    return idx;
  });
});
function oninputPhone(target) {
  target.value = target.value
    .replace(/[^0-9]/g, "")
    .replace(/(^02.{0}|^01.{1}|[0-9]{3,4})([0-9]{3,4})([0-9]{4})/g, "$1-$2-$3");
}

$(function () {
  /* 이메일 형식 맞는지 판단 */
  $("#emailError").hide();
  var reg_email =
    /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;
  $("#email").change(function () {
    const str = $("#email").val();
    const className = document.getElementById("email").classList;
    if (reg_email.test(str)) {
      className.remove("active");
      $("#emailError").hide();
      $("#emailError2").hide();
    } else {
      className.add("active");
      $("#emailError").show();
    }
  });

  /* 비밀번호와 비밀번호 확인이 일치하는지 비교 판단 */

  $("#pwError").hide();
  $("#password").change(function () {
    const pw = $("#password").val();
    const pwCheck = $("#passwordCheck").val();
    const pwClass = document.getElementById("password").classList;
    const pwcClass = document.getElementById("passwordCheck").classList;
    var reg = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
    // 최소 8자, 하나이상의 문자, 하나의 숫자 및 하나의 특수문자 정규식
    if (!reg.test(pw)) {
      alert("비밀번호 형식이 맞지 않습니다.");
      pwClass.add("active");
    } else {
      if (pw != pwCheck) {
        pwClass.add("active");
        pwcClass.add("active");
        $("#pwError").show();
      }
      if (pw == pwCheck) {
        pwClass.remove("active");
        pwcClass.remove("active");
        $("#pwError").hide();
      }
    }
  });
  $("#passwordCheck").change(function () {
    // 비밀번호 확인이 입력되면 동작
    const pw = $("#password").val();
    const pwCheck = $("#passwordCheck").val();
    const pwClass = document.getElementById("password").classList;
    const pwcClass = document.getElementById("passwordCheck").classList;
    if (pw != pwCheck) {
      pwClass.add("active");
      pwcClass.add("active");
      $("#pwError").show();
    }
    if (pw == pwCheck) {
      pwClass.remove("active");
      pwcClass.remove("active");
      $("#pwError").hide();
    }
  });

  /* 대학교를 선택할 경우 선택지를 더 보여줌 */
  $("#selboxDirect").hide();
  $("#education").change(function () {
    // 대학교를 선택할 경우 나타남
    if ($(this).find("option:selected").val() == "univ") {
      $("#selboxDirect").show();
    } else {
      $("#selboxDirect").hide();
    }
  });
});
