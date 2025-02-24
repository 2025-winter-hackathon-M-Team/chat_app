/*チャンネルを編集するモーダルの制御*/

const buttonUpdateChannelOpen = document.getElementById('update-channel-modalOpen');
const updateChannelModal = document.getElementById('update-channel-modal');
const buttonUpdateChannelClose = document.getElementById('add-channel-close-button');

if (updateChannelModal) {
  buttonUpdateChannelOpen.addEventListener('click', modalOpen);
   function modalOpen() {
    updateChannelModal.style.display = 'block';
   }
    
  buttonUpdateChannelClose.addEventListener("click", () => {
    updateChannelModal.style.display = "none";
  });
}

