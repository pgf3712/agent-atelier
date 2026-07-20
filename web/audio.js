(() => {
  "use strict";

  const toggle = document.querySelector("#audio-toggle");
  const label = document.querySelector("#audio-toggle-label");
  const volume = document.querySelector("#audio-volume");
  const status = document.querySelector("#audio-status");
  const track = document.querySelector("#ambient-track");
  if (!toggle || !label || !volume || !status || !track) return;

  let enabled = false;
  let cueContext;
  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  const translated = (key, fallback) => window.getAgentAtelierTranslation?.(key) || fallback;

  function text(key, english, spanish) {
    return translated(key, document.documentElement.lang === "es" ? spanish : english);
  }

  function currentLevel() {
    return Math.max(0, Math.min(1, Number(volume.value) / 100));
  }

  function updateInterface(state = enabled ? "playing" : "ready") {
    label.textContent = enabled
      ? text("audio.disable", "Mute cozy audio", "Silenciar ambiente")
      : text("audio.enable", "Enable cozy audio", "Activar ambiente acogedor");
    toggle.setAttribute("aria-pressed", String(enabled));
    const messages = {
      ready: text("audio.ready", "Ready — press the music button.", "Preparado — pulsa el botón de música."),
      playing: text("audio.playing", "Playing softly", "Reproduciendo suavemente"),
      muted: text("audio.muted", "Muted", "Silenciado"),
      blocked: text("audio.blocked", "Playback was blocked — use the player shown below.", "El navegador bloqueó la reproducción — utiliza el reproductor que aparece debajo.")
    };
    status.textContent = messages[state] || messages.ready;
    status.dataset.state = state;
  }

  async function toggleAudio() {
    if (enabled) {
      track.pause();
      enabled = false;
      updateInterface("muted");
      return;
    }
    track.volume = currentLevel();
    try {
      await track.play();
      enabled = true;
      updateInterface(track.volume === 0 ? "muted" : "playing");
      playCue("enable");
    } catch (_) {
      enabled = false;
      track.controls = true;
      track.classList.add("audio-fallback");
      updateInterface("blocked");
    }
  }

  function ensureCueContext() {
    if (!AudioContextClass) return undefined;
    if (!cueContext) cueContext = new AudioContextClass();
    if (cueContext.state === "suspended") cueContext.resume().catch(() => {});
    return cueContext;
  }

  function playTone(frequency, delay, duration, strength = 0.032) {
    if (!enabled) return;
    const context = ensureCueContext();
    if (!context) return;
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    const start = context.currentTime + delay;
    oscillator.type = "sine";
    oscillator.frequency.setValueAtTime(frequency, start);
    gain.gain.setValueAtTime(0.0001, start);
    gain.gain.exponentialRampToValueAtTime(strength * currentLevel(), start + 0.025);
    gain.gain.exponentialRampToValueAtTime(0.0001, start + duration);
    oscillator.connect(gain).connect(context.destination);
    oscillator.start(start);
    oscillator.stop(start + duration + 0.04);
  }

  function playCue(kind) {
    if (!enabled) return;
    const cues = {
      enable: [[523.25, 0, .11], [659.25, .1, .16]],
      click: [[440.00, 0, .055, .012]],
      chapter: [[523.25, 0, .12], [659.25, .11, .14], [783.99, .23, .22]],
      celebration: [
        [523.25, 0, .22, .024], [659.25, 0, .28, .018], [783.99, 0, .32, .016],
        [587.33, .34, .18, .022], [698.46, .50, .18, .022], [880.00, .66, .26, .022],
        [659.25, .96, .18, .024], [783.99, 1.12, .18, .024], [987.77, 1.28, .24, .024],
        [1046.50, 1.58, .52, .028], [783.99, 1.58, .58, .014], [659.25, 1.58, .62, .012]
      ]
    };
    (cues[kind] || cues.click).forEach(args => playTone(...args));
  }

  volume.value = localStorage.getItem("agent-atelier-audio-volume") || "24";
  track.volume = currentLevel();
  track.addEventListener("playing", () => {
    enabled = true;
    updateInterface(track.volume === 0 ? "muted" : "playing");
  });
  track.addEventListener("pause", () => {
    if (!enabled) return;
    enabled = false;
    updateInterface("muted");
  });
  track.addEventListener("error", () => updateInterface("blocked"));
  toggle.addEventListener("click", toggleAudio);
  volume.addEventListener("input", () => {
    track.volume = currentLevel();
    localStorage.setItem("agent-atelier-audio-volume", String(volume.value));
    if (enabled) updateInterface(track.volume === 0 ? "muted" : "playing");
  });
  document.addEventListener("click", event => {
    if (!enabled || event.target.closest("#audio-toggle")) return;
    if (event.target.closest("button, a, select")) playCue("click");
  });
  window.addEventListener("agent-atelier-locale-change", () => updateInterface());
  window.AgentAtelierAudio = {playCue};
  updateInterface("ready");
})();
