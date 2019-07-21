var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList;
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent;

let phrases = {
    'tomato': ['tomato','tomate','tomaten','gemüse'],
    'leopard': ['leopard','leoparden'],
    'dino': ['dino','dinos'],
    'turtle': ['turtle','schildkröte','schildkröten','turtles'],
    'frog': ['frog','frosch','frösche','frogs']
};

function randomPhrase() {
    var number = Math.floor(Math.random() * phrases.length);
    return number;
}

function startListening() 
{
    var buttonVoice = jQuery('#btn-voice');
    var voiceText = jQuery('#input-voice-label');

    //var grammar = '#JSGF V1.0; grammar phrase; public <phrase> = ' + phrase +';';
    var recognition = new SpeechRecognition();
    //var speechRecognitionList = new SpeechGrammarList();
    //speechRecognitionList.addF-romString(grammar, 1);
    //recognition.grammars = speechRecognitionList;
    recognition.lang = 'de-DE';
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;
    recognition.continuous = true;

    recognition.start();

    recognition.onresult = function(event) {
    // The SpeechRecognitionEvent results property returns a SpeechRecognitionResultList object
    // The SpeechRecognitionResultList object contains SpeechRecognitionResult objects.
    // It has a getter so it can be accessed like an array
    // The first [0] returns the SpeechRecognitionResult at position 0.
    // Each SpeechRecognitionResult object contains SpeechRecognitionAlternative objects that contain individual results.
    // These also have getters so they can be accessed like arrays.
    // The second [0] returns the SpeechRecognitionAlternative at position 0.
    // We then return the transcript property of the SpeechRecognitionAlternative object 

    var speechResult = event.results[0][0].transcript;
    var speechResultLower = event.results[0][0].transcript.toLowerCase();

    if(event.results[0].isFinal === true)
    {
        // console.log('---------------------------------------------------');
        // console.log('Confidence: ' + event.results[0][0].confidence);
        // console.log(event.results[0]);

        for (var animal in phrases) {
            phrases[animal].forEach(element => {
                if(speechResultLower.includes(element))
                {
                    console.log(animal+" wurde erkannt");
                    jQuery("button[id^='animal_']").removeClass("animal-selected");
                    jQuery("button[id^='animal_"+animal+"']").addClass("animal-selected");
                    selectedAnimal = 'animal_'+animal;
                    jQuery("#btn-start").attr('disabled',false);
                    webserver.handleButtonStart(this);
                }
            });
        }
        
        voiceText.text(speechResult);
        recognition.stop();
    }
    }

    recognition.onspeechend = function() {
    recognition.stop();
    console.log('onspeechend');
    }

    recognition.onerror = function(event) {
    console.log(event.error);
    //diagnosticPara.textContent = 'Error occurred in recognition: ' + event.error;
    }

    recognition.onaudiostart = function(event) {
        //Fired when the user agent has started to capture audio.
        // console.log('SpeechRecognition.onaudiostart');
    }

    recognition.onaudioend = function(event) {
        //Fired when the user agent has finished capturing audio.
        // console.log('SpeechRecognition.onaudioend');
    }

    recognition.onend = function(event) {
        //Fired when the speech recognition service has disconnected.
        // console.log('SpeechRecognition.onend');
    }

    recognition.onnomatch = function(event) {
        //Fired when the speech recognition service returns a final result with no significant recognition. This may involve some degree of recognition, which doesn't meet or exceed the confidence threshold.
        // console.log('SpeechRecognition.onnomatch');
    }

    recognition.onsoundstart = function(event) {
        //Fired when any sound — recognisable speech or not — has been detected.
        // console.log('SpeechRecognition.onsoundstart');
    }

    recognition.onsoundend = function(event) {
        //Fired when any sound — recognisable speech or not — has stopped being detected.
        // console.log('SpeechRecognition.onsoundend');
    }

    recognition.onspeechstart = function (event) {
        //Fired when sound that is recognised by the speech recognition service as speech has been detected.
        console.log('SpeechRecognition.onspeechstart');
    }
    recognition.onstart = function(event) {
        //Fired when the speech recognition service has begun listening to incoming audio with intent to recognize grammars associated with the current SpeechRecognition.
        // console.log('SpeechRecognition.onstart');
    }
}
