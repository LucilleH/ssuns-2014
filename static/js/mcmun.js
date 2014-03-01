$(document).ready(function() {
	
	 $('.slideshow').cycle({
		fx: 'fade'
	});
	// for registration if it's the first time the school attend ssuns, then ask them more question
	$('#registration_form select[id^="id_first_time"]').change(function () {
		var result = $(this).find('option:selected').val();
		if(result === 'True') {
			$('#howYouHear').show()		
		}
		else {
			$('#howYouHear').hide()	
		}
	});
	//also for registration for referring from other school. baddddddd
	$('#registration_form select[id^="id_how_you_hear"]').change(function () {
		var result = $(this).find('option:selected').val();
		if(result === 'another_school') {
			$('#anotherschool').show()
			$('#other').hide()	
		}
		if(result === 'other') {
			$('#other').show()	
			$('#anotherschool').hide()
		}
	});


	// Staff coordinator application form
	if ($('#staff-coordinator-form').length) {
		// Hide the ones that don't always need to be filled
		$('#id_occc_experience').parent().parent().hide();
		$('#id_event_experience').parent().parent().hide();

		// Show them if the right thing is selected as a preferred position
		$('#staff-coordinator-form select[id^="id_preferred_position"]').change(function () {
			var selected = $(this).find('option:selected').val();

			// Truly awful
			if (selected === 'events-coord' || selected === 'events-tl') {
				$('#id_event_experience').parent().parent().show();
			} else {
				// lol
				if (!$('#staff-coordinator-form select[id^="id_preferred_position"] option[value^="events"]:selected').length) {
					$('#id_event_experience').parent().parent().hide();
				}
			}

			if (selected === 'occc') {
				$('#id_occc_experience').parent().parent().show();
			} else {
				if (!$('#staff-coordinator-form select[id^="id_preferred_position"] option[value^="occc"]:selected').length) {
					$('#id_occc_experience').parent().parent().hide();
				}
			}
		});
	}

	// If any element on the page has an ID of collapsible, make the h2+ headings collapsible
	if ($('#collapsible').length) {
		var headings = 'h2,h3,h4,h5,h6';

		$(headings).each(function (index, heading) {
			// Add the [-] / [+] thing
			this.innerHTML += ' <a href="#" class="toggle-collapse">[-]</a>';
		});

		$('#content').on('click', '.toggle-collapse', function (event) {
			var heading = this.parentNode;
			var headingTag = heading.localName;

			// Get all the headings at this level or bigger
			var relevantHeadings = headings.substr(0, headings.indexOf(headingTag) + 2);
			var section = $(heading).nextUntil(relevantHeadings);

			// kind of buggy - if a child is hidden and a parent is hidden then shown, it won't match up
			if ($(this).hasClass('collapsed')) {
				$(section).show();
				this.innerText = '[-]';
			} else {
				$(section).hide();
				this.innerText = '[+]';
			}

			$(this).toggleClass('collapsed');

			return false;
		});
	}

	


	// Show the person's title upon hovering over the photo
	$('#sec-bios').delegate('.photo', 'mouseenter', function (event) {
		var title = $(this).next().find('h3').text();
		$(this).append('<div class="title-hover">' + title + '</div>');
		$('.title-hover').fadeIn(300);
	});

	$('#sec-bios').delegate('.photo', 'mouseleave', function (event) {
		$('.title-hover').remove();
	});

	$('#sec-bios').delegate('.photo', 'click', function (event) {
		$('.active').removeClass('active');
		$('.bio').hide();
		$(this).addClass('active').next().show();
	});

	var delegationFee = 75;

	$('#fee-calculator').delegate('select', 'change', function (event) {
		var numDelegates = parseInt($('#num-delegates option:checked').val(), 10);
		var registrationType = $('#registration-type option:checked').val();

		// Only show the fee information stuff when everything has been selected
		if (numDelegates > 0 && registrationType !== '') {
			var delegateFee, totalFee, deposit, remainder;

			switch (registrationType) {
				case 'priority':
					delegateFee = 80;
				break;
				case 'regular':
					delegateFee = 95;
				break;
				case 'international':
					delegateFee = 50;
				break;
			}

			if (delegateFee) {
				totalFee = numDelegates * delegateFee + delegationFee;
				deposit = delegationFee + (numDelegates * delegateFee) * 0.5;
				remainder = totalFee - deposit;
				$('#fee-information').text('Your total fee, for ' + numDelegates + ' delegates and ' + registrationType + ' registration, is $' + totalFee.toFixed(2) + '. If you wish to pay using the tiered system, your deposit would be $' + deposit.toFixed(2) + ', and the remainder would be $' + remainder.toFixed(2) + '.');
			} else {
				// Someone is mucking about with the form
				$('#fee-information').text("Please stop messing with the form. There's nothing interesting here.");
			}
			$('#fee-information').show();
		}
	});

	/*
	// Handle stuff for the registration form
	var priorityOption = $('#priority-dt');
	if (priorityOption.length) {
		// Has to be done this way for now because dl only allows dt, dd (fix later)
		priorityOption.hide().next().hide();
		$('#id_country').change(function () {
			var country = $(this).val();

			// The priority registration option is only valid for North America
			if (country === 'CA' || country === 'US') {
				priorityOption.show().next().show();
			} else {
				priorityOption.hide().next().hide();
			}
		});
	}
	*/
});
