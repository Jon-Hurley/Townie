<script>
    const State = {
        start,
        running,
        pause,
        reset
    }

    let state = State.start;

    let startTime = 0;
    let totalTime = 0;
    let endTime = 0;
    let interval;

    //formatted time 
    $: hours = `00${((totalTime/1000/60/60)%60)}`.slice(-2);
    $: minutes = `00${((totalTime/1000/60)%60)}`.slice(-2);
    $: seconds = `00${((totalTime/1000)%60)}`.slice(-2);
    $: formattedTime = `${hours}:${minutes}:${seconds}`;

    /* Adds this all to backend functions like start game, end game
    const _startTimer = async() => {
        state = State.running;
        await startTimer();
    }

    const _pauseTimer = async() => {
        state = State.pause;
        await pauseTimer();
    }

    const _resetTimer = async() => {
        state = State.running;
        await endTimer();
    }
    */
</script>

<div class="glass p-2 text-white border border-text-white">
    <h1 class="mb-2 border-b border-white">
        Total Time
    </h1>
    ${formattedTime}
</div>