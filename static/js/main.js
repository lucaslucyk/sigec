
const inputRange = $('#html-input-range');
const inputText = $('#integCtrl');

let htmlInputRange = {
  idNotThere : '<p>Nota: No existe tag con id html-input-range</p>',
  init () {
    if (inputRange.length > 0) {
      let inputRanges = $('#html-input-range');
      inputRanges.parent().addClass('html-inupt-range');
      // if too many input ranges there for now hiding this part.
      // inputRanges.each(function( index ) {
      //   let $this = $(this);
      // });
      let $this = inputRanges;

    } else {
      $('input[type=range]').parent().append(htmlInputRange.idNotThere);
    }

    updatePrice(inputRange.val());
  },
  options (inputs) {
    htmlInputRange.init();
    let options = inputs;
    // custom tracker
    $('input[type=range]').parent().addClass('html-input-range-custom');
    $('input[type=range]').parent().append('<div class="hir-tracker-bg"></div><div class="hir-tracker-thumb"></div>');
    let min = 1;
    let max = $('input[type=range]').attr('max');
    if (options.tooltip === true) {
      if (options.max) {
        max = options.max;
        $(inputRange).attr({
          max: options.max
        });
      }
      $('input[type=range]').parent().append('<div class="tooltip">'+ min +'</div>');
    }
    if (options.labels === true) {
      $(inputRange).parent().append('<ul class="hir-labels"></ul>');
      let setWidth;
      if (options.max) {
        setWidth = options.max/10;
      } else {
        setWidth = max/10;
      }
      for (let i = 0; i < setWidth; i++) {
        $('.hir-labels').append('<li class="col-'+ setWidth +' "></li>');
      }
    }
  }
}

$(inputText).keypress(function(e){
  var code = (e.code ? e.keyCode : e.which);
  if (code == 13){
    var cv = parseInt($(inputText).val());
    var min = parseInt($('input[type=range]').attr('min'));

    //console.log(cv);

    if (cv < min || !cv) {
      inputText.val("50");
      cv = 50;
    }

    //if (cv >= min) {
    var max = parseInt($('input[type=range]').attr('max'));
    // console.log(cv);
    // console.log(max);

    if (cv >= max) {
      contactus();
    } else {
      showPrice();

      let inputMax = 100 / inputRange.attr('max');
      let trackerTooltipMove = (cv * inputMax);
      $('.html-inupt-range .tooltip').css('left', trackerTooltipMove + '%');
      $('.html-input-range-custom .hir-tracker-thumb').css('width', trackerTooltipMove + '%');
      // updating tooltip value based on the range from to.
      $('.html-inupt-range .tooltip').text(inputRange.val());

      const price = get_precios(cv);
    }
    //}
  }
});

$(inputRange).on("mouseup touchend", inputRange, function (e) {
  //actualizo el precio por persona y el total únicamente si suelto el mouse
  const cv = get_precios(inputRange.val());

});

$(inputRange).on('input change', inputRange, function (e) {
  /*
  * splitting 100 by input range max value
  * for active tracker and tooltip position.
  */
  var max = $('input[type=range]').attr('max');
  let inputMax = 100 / inputRange.attr('max');
  let trackerTooltipMove = (inputRange.val() * inputMax);
  $('.html-inupt-range .tooltip').css('left', trackerTooltipMove + '%');
  $('.html-input-range-custom .hir-tracker-thumb').css('width', trackerTooltipMove + '%');
  // updating tooltip value based on the range from to.
  $('.html-inupt-range .tooltip').text(inputRange.val());

  //console.log(inputRange.val());
  updatePrice(inputRange.val());

  if (inputRange.val() == max) {
    contactus();
  } else {
    showPrice();
  }
});

function contactus () {
  $("#precio-total").hide();
  $("#precio-contacto").fadeIn(300);
  $("#showPrice").attr('disabled','true');
}

function showPrice() {
  $("#precio-total").show();
  $("#precio-contacto").hide();
  $("#showPrice").removeAttr('disabled');
}

async function get_precios(employees){

  var url = window.location.origin + '/get_offer/';
  //localhost:8000/get_offer/End%20User/36/Propio/200/

  $.each($(".data-send"), function(index, value){
      if (value.getAttribute("tv-value") !== null){
        url += value.getAttribute("tv-value") + "/";
      }
      if (value.getAttribute("plan-value") !== null){
        url += value.getAttribute("plan-value") + "/";
      }
      if (value.getAttribute("hw-value") !== null){
        url += value.getAttribute("hw-value") + "/";
      }
    });

  url += employees +'/';
  // final url is 
  // <baseUrl>/get_precios/<str:tipo_venta>/<str:plan>/<str:hardware>/<str:modulos>/<int:empleados>/

  //await console.log(url);

  const res = await fetch(url);
  const json = await res.json();

  //console.log(json.form.vm_por_capita);
  $('#to').text(json.form.pv_capita.toFixed(2)); //valor por capita
  $('#total-price').text((json.form.pv_mensual).toFixed(2)); //valor total por mes
}

function updatePrice(currentValue) {
  //update price
  //const cv = get_precios(currentValue);

  $('#integrantes').text(currentValue);
  $('#integCtrl').val(currentValue);
  $('input[name="employees"]').val(currentValue);
}

//at click on checks
$(".click-change-view").click(function() {
    
  //check if is not disabled
  if (!this.hasAttribute('disabled')){

    //remove selected class of everything ele
    $.each($(this).attr("data-change").split(" "), function(index, value) {
      $("#" + value).removeClass('description text-center data-send').addClass('price');
    });


    if (this.hasAttribute('data-disable')){
      //console.log("tiene!");
      $.each($(this).attr("data-disable").split(" "), function(index, value) {
        $("#" + value).attr("disabled", "disabled");//.off('click');
      });
    }

    if (this.hasAttribute('data-eneable')){
      //console.log("tiene!");
      $.each($(this).attr("data-eneable").split(" "), function(index, value) {
        $("#" + value).removeAttr("disabled");
      });
    }

    if (this.hasAttribute('data-activate')){
      //console.log("tiene!");
      $.each($(this).attr("data-activate").split(" "), function(index, value) {
        $("#" + value).removeClass('price').addClass('description text-center data-send');
      });
    }

    //add selected class
    $(this).removeClass('price').addClass('description text-center data-send');

    const cv = get_precios($("#integCtrl").val());
  }
});

$("#integCtrl").click(function(){
  $(this).val("");
});

$(function(){
  //initial input range position
  var cv = parseInt($(inputText).val());
  let inputMax = 100 / inputRange.attr('max');
  let trackerTooltipMove = (cv * inputMax);
  $('.html-inupt-range .tooltip').css('left', trackerTooltipMove + '%');
  $('.html-input-range-custom .hir-tracker-thumb').css('width', trackerTooltipMove + '%');

  //update current year for rights reserved
  var now = new Date();
  $("#currentYear").text(now.getFullYear());

  // var userLang = navigator.language || navigator.userLanguage;
  // console.log(userLang);

});
