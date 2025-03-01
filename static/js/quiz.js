const body = document.querySelector('body');
const imgcontainer = document.createElement('div');

function chimg(imgUrl, elt) {
    body.appendChild(imgcontainer);
    imgcontainer.innerHTML = '<img src=' + imgUrl + '>';
    imgcontainer.classList.add('displayimg');
    imgcontainer.style.top = (elt.getBoundingClientRect().top + 35) + 'px';
    
    let difference = document.documentElement.clientWidth - elt.getBoundingClientRect().left;

    if(difference < 150){
    imgcontainer.style.right = '20px';
    }
    else{
    imgcontainer.style.left = elt.getBoundingClientRect().left + 'px';
    }

    imgcontainer.style.animation = 'fadeIn .8s';
}

function removeimg() {
    imgcontainer.style.animation = 'fadeOut .8s';
    body.removeChild(imgcontainer);
}
