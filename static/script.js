function fun_onload(){
    var audioWeWantToUnlock = document.getElementById('songfile');
    document.body.addEventListener('touchstart', function() {
        if(audioWeWantToUnlock) {
        audioWeWantToUnlock.pause()
        audioWeWantToUnlock.play()
        audioWeWantToUnlock = null
    }
    }, false)
}

function showloading(){
    document.getElementById('loading').innerText="Okay, Searching..."
}

