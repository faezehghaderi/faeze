$(document).ready(function(){
    $(".icon-bg").click(function () {
        $(".btn").toggleClass("active");
        $(".icon-bg").toggleClass("active");
        $(".container").toggleClass("active");
        $(".box-upload").toggleClass("active");
        $(".box-caption").toggleClass("active");
        $(".box-tags").toggleClass("active");
        $(".private").toggleClass("active");
        $(".set-time-limit").toggleClass("active");
        $(".button").toggleClass("active");
    });

	$('#typeOfGlass').on('change', function(){
	   console.log($('#typeOfGlass').val());
		$('#glassWidth').html('');
		if($('#typeOfGlass').val()==15){
			$('#glassWidth').append('<option value="19">19</option>');
			$('#glassWidth').append('<option value="20">20</option>');
			$('#glassWidth').append('<option value="21">21</option>');
		}else{
			$('#glassWidth').append('<option value="6">6</option>');
			$('#glassWidth').append('<option value="7">7</option>');
			$('#glassWidth').append('<option value="8">8</option>');
			$('#glassWidth').append('<option value="9">9</option>');
		}
	});


    $(".button").click(function () {
        $(".button-overlay").toggleClass("active");
    });

    $(".iconmelon").click(function () {
        $(".box-upload-ing").toggleClass("active");
        $(".iconmelon-loaded").toggleClass("active");
    });

    $(".private").click(function () {
        $(".private-overlay").addClass("active");
        $(".private-overlay-wave").addClass("active");
    });
});