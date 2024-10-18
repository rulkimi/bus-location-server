export const formatTime = timestamp => {
  return new Date(timestamp * 1000).toLocaleTimeString('en-MY', { timeZone: 'Asia/Kuala_Lumpur', hour: '2-digit', minute: '2-digit', hour12: true });
}