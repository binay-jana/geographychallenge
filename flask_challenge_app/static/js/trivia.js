$("#creation_answers_form").submit(function(event) {
  event.preventDefault();
  return false;
});
var counter;
(function($) {
    $.fn.flash_message = function(options) {
      options = $.extend({
        text: 'Done',
        time: 1000,
        how: 'before',
        class_name: ''
      }, options);
      
      return $(this).each(function() {
        if( $(this).parent().find('.flash_message').get(0) )
          return;
        
        var message = $('<span />', {
          'class': 'flash_message ' + options.class_name,
          text: options.text
        }).hide().fadeIn('fast');
        
        $(this)[options.how](message);
        
        message.delay(options.time).fadeOut('normal', function() {
          $(this).remove();
        });
        
      });
    };
})(jQuery);

(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/all.js";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// async init once loading is done
window.fbAsyncInit = function() {
  FB.init({
    appId: 1673890419499781,
    xfbml: true,
    version    : 'v2.3'
  });
};

var created_correct_answers = {};

window.onload = function() {
    $('#faq').click(function(event) {
        $('#faq_div').toggle();
      }
    );

    $('input#answer_box').bind("change paste keyup", function() {
        var answer = $.trim($('input#answer_box').val().toLowerCase());
        if(question.answers[answer] != null){
          var answered_item = question.answers[answer];
          if ($.inArray(answered_item, correctly_answered)==-1) {
            append_answer(answered_item);
            $('input#answer_box').val('');
          }
        }
    });

    $('#access_code_form').submit(function (event) {
        event.preventDefault();
        var answer = $.trim($('input#answer_box').val().toLowerCase());
        var error_string = null;
        if(question.answers[answer] != null){
            var answered_item = question.answers[answer];
            if ($.inArray(answered_item, correctly_answered)==-1) {
              append_answer(answered_item);
            } else {
              error_string = "You already entered " + question.names[answered_item];
            }
        } else {
            error_string = answer + " is not right answer.";
        }
        if(error_string!=null && answer) {
            append_wrong_answer(answer);
        }
        $('input#answer_box').val('');        
        return false;
    });
    function addToAnswers(event) {
        event.preventDefault();
        var answer = $.trim($('input#creation_answer_box').val().toLowerCase());
        if(created_correct_answers[answer] || !answer) {
          return;
        }
        created_correct_answers[answer] = 1;
        $('input#creation_answer_box').val('');
        $('#quiz_creation_answers').show();
        var $answer_el = $('<div />');
        $answer_el.addClass("answered_item").text(answer);
        var $cross = $('<img src="/static/images/x.png" width="10px" class="x_created_answers"/>');
        $cross.click(function(event) {
          $answer_el.remove();
          delete created_correct_answers[$answer_el.text()];
          console.log(created_correct_answers);
        });
        $answer_el.append($cross)
        $('#quiz_creation_answers').append($answer_el);
        validateAnswers();
    }
    $('#add_answer').click(addToAnswers);
    $('#creation_answer_box').keypress(function(e) {
      if(e.which===13){
        addToAnswers(e);
      }

    });
    $('#giveup').click(function(e) {
      clearInterval(counter);
      showResults();
    })

    function append_answer(answered_item) {
        $('#answer_boxes').show();
        $answer_el = $('<span />');
        var full_name = question.names[answered_item];
        correctly_answered.push(answered_item);
        $('#scored_points').text(correctly_answered.length);
        $answer_el.addClass("answered_item").text(full_name);
        $('#entered_answers').append($answer_el);
        if (correctly_answered.length==question.names.length) {
          clearInterval(counter);
          showResults();
        }
    }

    function append_wrong_answer(answered_item) {
        console.log(answered_item);
        $('#answer_boxes').show();
        $answer_el = $('<span />');
        $answer_el.addClass("missed_item").text(answered_item);
        $('#entered_answers').append($answer_el);
    }

    function stopChallenge() {
        $('#answer_box').prop('disabled', true);
        $('#submit_button').prop('disabled', true);
    }

    function timesUp() {
        stopChallenge();
        showAnswers();
        if(correctly_answered.length==question.names.length) {
            console.log('YAY');
        } else {
            console.log('BOO');
        }
    }

    function populateQuestion() {
        $('#number_of_seconds').text(time)
        $('#challenge_prompt').html(
          str_replace(['number'],
            [question.passing_score],
            "Your Challenge: " + question.prompt
          ));
        $('#scored_points').text(0);
        $('#required_points').text(question.passing_score);
    }
    populateQuestion();
    populateFAQ();
}

function populateFAQ() {
    var text = "<div class='faq_item'>" +
    "<div class='faq_question'>How is my donation going to be used?</div>" +
    "<div class='faq_answer'>Jana is going to hand over the collected donations to the <a href='http://pmrelief.opmcm.gov.np/about.aspx' target='_blank'>Nepali Prime Minister Disaster Relief Fund</a> and the <a href='http://www.unicef.org/infobycountry/nepal.html' target='_blank'>UNICEF</a>. These organizations have been helping the victims of the earthquake since the very first day after the earthquake. Both of these organizations are transparent and well regulated.</div>" +
    "</div>" +
    "<div class='faq_item'>" +
    "<div class='faq_question'>What is Jana? Why is the company organizing this fundraiser?</div>" +
    "<div class='faq_answer'>We are a for-profit internet startup based in Boston, USA. You can <a href='http://www.forbes.com/sites/ilyapozin/2015/05/06/this-is-facebooks-biggest-competitor-in-emerging-markets' target='_blank'>read about us here</a>. Our engineers came up with the idea for the fundraiser and the team implemented it during our quaterly hackathon day. While this fundraiser is not part of our business, we are happy to be able to organize the fundraiser to raise awareness and support for the millions affected by the disaster.</div>" +
    "</div>" +
    "<div class='faq_item'>" +
      "<div class='faq_question'>Who created the trivia questions?</div>" +
      "<div class='faq_answer'>The questions are user generated. You too can create your own challenge. Just avoid profane and/or offensive content. Use your moral judgement.</div>" +
    "</div>" +
    "<div class='faq_item'>" +
      "<div class='faq_question'>I cannot donate. How can I help?</div>" +
      "<div class='faq_answer'>It is okey if you cannnot donate. You can still help us by challenging your friends and creating new trivias.</div>" +
    "</div>" +
    "<div class='faq_item'>" +
      "<div class='faq_question'>I do not know what kind of trivia questions are interesting. Do you have any suggestions?</div>" +
      "<div class='faq_answer'>Think about the topics your friends care about. It could be about your highschool, sports, actors, movies, or you.</div>" +
    "</div>";
    $('#faq_div').html($(text));
}

function get_nominated_question() {
    return $('#challenge_selection').val();
}

function gogogo() {
    var url = window.location.href;
    var q = get_nominated_question();
    if (q!=="default") {
      url = 'http://' + window.location.host + '/' + q;
    } else {
      url = window.location.href;
    }
    showFacebookUI(url);
}

function showCreatedQIDShare() {
  if(created_qid!==null) {
    return showFacebookUI('http://' + window.location.host + '/' + created_qid);
  }
  return gogogo();
}

function showFacebookUI(url){
    url = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url);
    window.open(url, 'newWin','width=800,height=600');
}

function start_timer() {
    var time_left = time;
    function timer() {
        time_left -= 1;
        if (time_left < 0) {
            clearInterval(counter);
            showResults();
            return;
        }
        $('#time_left').text(time_left);
    }
    $('#time_left').text(time_left);
    counter = setInterval(timer, 1000);
}

function str_replace(replaceArray, replaceWith, myString) {
  for(var i = 0; i < replaceArray.length; i++) {
    myString = myString.replace(new RegExp('{' + replaceArray[i] + '}', 'gi'), replaceWith[i]);
  }
  return myString;
}

// function populate_nomination_challenges() {
//   var options = $('#challenge_selection');
//   $.each(questions, function() {
//     var question_item = str_replace(
//       ['number'],
//       [this.passing_score],
//       this.description
//     );
//     options.append($("<option />").val(this.question_id).text(question_item));
//   });
// }

function startquiz() {
  $('#answer_form').show();
  $('#start_button').hide();
  $('#donation_button').hide();
  start_timer();
}


function populateAnswers() {
    for (index in question.names) {
        if($.inArray(parseInt(index), correctly_answered)==-1) {
            $answer_el = $('<span />');
            var full_name = question.names[index];
            $answer_el.addClass("missed_item").text(full_name);
            $('#final_missed_answers').append($answer_el);
        } else {
            $answer_el = $('<span />');
            var full_name = question.names[index];
            $answer_el.addClass("answered_item").text(full_name);
            $('#final_entered_answers').append($answer_el);
        }
    }
}


function showResults() {
  var result_header = "Congratulations, you passed the Challenge";
  if (correctly_answered.length < question.passing_score) {
    result_header = "You needed " + question.passing_score + " to pass.. you only got " + correctly_answered.length;
  } else {
    result_header = "Congratulations you passed. Challenge your friends next."
  }
  populateAnswers();
  $('#challenge_prompt').text(result_header);
  $('#challege_subtext').hide();
  $('#answer_form').hide();
  $('#donation_button').show();
}

function load_create() {
  $('#challenge_box').hide();
  $('#share_box').hide();
  $('#create_box').show();
}

function cancelcreate() {
  $('#challenge_box').show();
  $('#share_box').show();
  $('#create_box').hide(); 
  $("html, body").animate({ scrollTop: $(document).height() }, "fast");
}

function validate() {
  valid = true;
  valid = validateChallenge() && valid;
  valid = validateAnswers() && valid;
  valid = validatePassingScore() && valid;
  return valid;
}

function validateChallenge() {
  var $input = $('#created_list_question');
  var $error = $('#challenge_error');
  var c = $input.val();
  console.log(c);
  if (c===null || c==="") {
    $input.addClass("error");
    $error.text("You must add a description.");
    return false;
  }
  if (c.length>=200) {
    $input.addClass("error");
    $error.text("Description cannot be more than 200 charater long.");
    return false;
  }
  $error.text('');
  $input.removeClass("error");
  return true;
}

function validateAnswers() {
  var $input = $('#creation_answer_box');
  var $error = $('#possible_answers_error');
  console.log('this is called');
  if(Object.keys(created_correct_answers).length === 0) {
    $input.addClass("error");
    $error.text("Please enter at least one correct answer.");
    return false;
  }
  $error.text('');
  $input.removeClass("error");
  return true;
}

function validatePassingScore() {
  var $input = $('#passing_score');
  var p = $input.val();
  var $error = $('#passing_score_error');
  if (isNaN(p)) {
    $input.addClass("error");
    $error.text("Passing score must be a number.");
    return false;
  }
  if (p <= 0) {
    $input.addClass("error");
    $error.text("Passing score must be a number greater than 0.");
    return false;
  }
  if (p > Object.keys(created_correct_answers).length) {
    $input.addClass("error");
    $error.text("Passing score must be less than the total number of answers.");
    return false;
  }
  $error.text('');
  $input.removeClass("error");
  return true;
}

function createquiz() {
  var valid = validate();
  if (!valid) {
    return;
  }
  $('#submit_create').prop('disabled', true);
  $('#cancel_create').prop('disabled', true);
  $('#creation_form').hide();
  $('#question_creation_loading').show();
  var name = $('#name').val();
  var prompt = $('#created_list_question').val();
  var question_answer_sets = [];
  var passing_score = $('#passing_score').val();
  var to_send = {
    'name': name,
    'passing_score': passing_score,
    'prompt': prompt,
    'correct_names': created_correct_answers
  };
  $.ajax({
      url: 'create_challenge',
      data: JSON.stringify(to_send),
      type: "POST",
      success: function(data) {
          created_qid = data['question_id'];
          afterCreationSuccess();
      },
      error: function(jqXHR, textStatus, errorThrown) {
          afterCreationFailure();
      },
      contentType : 'application/json',
      dataType: "json"
  });
}

function getCreatedURL() {
  return 'http://' + window.location.host + '/' + created_qid;
}
function afterCreationSuccess() {
  $('#submit_create').hide();
  $('#cancel_create').hide();
  $('#question_creation_loading').hide();
  $('#share_created_question').show();
  var url = getCreatedURL();
  var $link = $('<a></a>');
  $link.prop('href', url);
  $link.text(url);
  $('#created_question_link').html($link);
}
function afterCreationFailure() {
  $('#submit_create').prop('disabled', false);
  $('#cancel_create').prop('disabled', false);
  $('#creation_form').show();
  $('#question_creation_loading').hide();
}