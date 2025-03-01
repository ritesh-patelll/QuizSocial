document.addEventListener('DOMContentLoaded', async function () {
    const copyTextBtn = document.getElementById('copy-text-btn')
    const copyImgBtn = document.getElementById('copyBtn')

    const img = document.querySelector('.quizsocial-img2')

    const setToClipboard = blob => {
        const data = [new ClipboardItem({ [blob.type]: blob })]
        document.getElementById('in-chara2').style.display = "flex";
        return navigator.clipboard.write(data)
    }

    /**
     * @param Blob - The ClipboardItem takes an object with the MIME type as key, and the actual blob as the value.
     */

    copyImgBtn.addEventListener('click', async () => {
    try {
        const response = await fetch(img.src)
        const blob = await response.blob()
        await setToClipboard(blob)
        setTimeout(() => {  document.getElementById('in-chara2').style.display = "none"; }, 1000);
    } catch (error) {
        console.error('Something wrong happened')
        console.error(error)
    }
    })
})