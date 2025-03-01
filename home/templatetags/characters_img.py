from django.template.defaulttags import register

@register.filter(name='characters_img')
def characters_img(tci, wos):
    finial_word = wos
    for cnk in tci.keys():
        if cnk in wos:
            if cnk in wos:
                if ' ' + cnk in wos:
                    finial_word = finial_word.replace(' ' + cnk, '&nbsp;<span id="https://quiz-social-static-and-media-files.s3.amazonaws.com/static/img/all_casts/' + tci[cnk] + '.jpg" class="btn btn-dark btn-outline-success" style="border-bottom: 2px dashed #000;cursor: pointer;" onClick="chimg(this.id, this)" onmouseenter="chimg(this.id, this);" onmouseout="removeimg();">' + cnk + '</span>')
                else:
                    finial_word = finial_word.replace(cnk, '<span id="https://quiz-social-static-and-media-files.s3.amazonaws.com/static/img/all_casts/' + tci[cnk] + '.jpg" class="btn btn-dark btn-outline-success" style="border-bottom: 2px dashed #000;cursor: pointer;" onClick="chimg(this.id, this)" onmouseenter="chimg(this.id, this);" onmouseout="removeimg();">' + cnk + '</span>')
    return finial_word
