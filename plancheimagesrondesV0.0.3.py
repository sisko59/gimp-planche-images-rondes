#!/usr/bin/env python

# Planche a photo ronde en GIMP Python

from gimpfu import *
import os

def imagesDuDossier(repertoire) :
    result = []
    allFileList = os.listdir(repertoire)
    for fname in allFileList:
        fnameLow = fname.lower()
        if fnameLow.count('.jpg') > 0:
            result.append(fname)    
    return result

def detectRapportDeCadre(image, size) :
    hauteur = pdb.gimp_image_height(image)
    largeur = pdb.gimp_image_width(image)

    #on prend le plus petit coté
    if (hauteur < largeur):
        return hauteur / size
    else :
        #largeur la plus grande ou les cotes sont identiques
        return largeur / size

#==============================================================================
#===================== calculate papersize in pixels ==========================
#===================== given sizes are mm =====================================
#==============================================================================
def CalcPaperSize(ContactSize, dpi):
    if (ContactSize == 0):             #Jumbo
        width,height = (102,152)
    elif (ContactSize == 1):           #6x8
        width,height = (152,203)
    elif (ContactSize == 2):           #8x10
        width,height = (203,254)        
    elif (ContactSize == 3):           #A4
        width,height = (210,297)
    elif (ContactSize == 4):           #A3
        width,height = (297,420)
    elif (ContactSize == 5):           #A2
        width,height = (420,594)
    elif (ContactSize == 6):           #A1
        width,height = (594,841)
    elif (ContactSize == 7):           #A0
        width,height = (841,1189)
    elif (ContactSize == 8):           #Letter
        width,height = (216,279)
    elif (ContactSize == 9):           #Legal
        width,height = (216,356)
    elif (ContactSize == 10):           #Tabloid
        width,height = (279,432)
    elif (ContactSize == 11):           #banner A4 width
        width,height = (210,1000)
    elif (ContactSize == 12):           #banner A3 width
        width,height = (297,1000)
    else:
        width,height = (210,297)
        Log("error in pagesize, pagesize doesnot exist")

    width = int((width/25.4)*dpi)              # calculate width in px
    height = int((height/25.4)*dpi)            # calculate height in px

    return width, height                       #size in pixels

def picture_square_sheet(size, repertoire) :
    #dans la console gimp pour image courrante
    #image = gimp.image_list()[0]
    #repertoire avec image pour tester
    repertoire = '/home/francis/Images'
    dpi = 150

    #taille feuille creer
    width,height = CalcPaperSize(3, dpi)
    sheetimg = gimp.Image(width,height,RGB)
    sheetimg.resolution = (float(dpi), float(dpi))

    # Cree un nouveau layer sans fond
    layer = pdb.gimp_layer_new(sheetimg, width, height, 1, 'layer', 100, 0)
    #ajoute le layer à l'image
    sheetimg.add_layer(layer,0)    

    lesImages = imagesDuDossier(repertoire)
    #coordonnees correspondant a la position en haut a gauche
    posXImageSuivante = -500
    posYImageSuivante = -700
    nbImageSurLigne = 0

    for nomImage in lesImages :
        nbImageSurLigne = nbImageSurLigne+1
        #nom de la premiere image
        #charge l'image
        cheminImage = repertoire+'/'+nomImage
        image = pdb.gimp_file_load(cheminImage, cheminImage)

        hauteur = pdb.gimp_image_height(image)
        largeur = pdb.gimp_image_width(image)

        rapportDeCadre = detectRapportDeCadre(image, size)

        newHauteur = hauteur / rapportDeCadre
        newLargeur = largeur / rapportDeCadre
        #redimensionne l'image
        pdb.gimp_image_scale(image, newLargeur, newHauteur)

        #selection elliptique depuis en haut a gauche
        pdb.gimp_image_select_ellipse(image, 0, 0, 0, size, size)
        #copie la selection
        pdb.gimp_edit_copy(image.active_layer)

        #copie la selection
        selection = pdb.gimp_edit_paste(layer,True)

        selection.translate(posXImageSuivante, posYImageSuivante)
        pdb.gimp_floating_sel_anchor(selection)

        #retire l'image de la memoire
        gimp.delete(image)
        posXImageSuivante = posXImageSuivante + 200

        if (nbImageSurLigne == 6) :
            nbImageSurLigne = 0
            posYImageSuivante = posYImageSuivante + 200
            posXImageSuivante = -500

    # Create a new image window
    gimp.Display(sheetimg)
    # Affiche l'image
    gimp.displays_flush()

register(
    "python_fu_picture_square_sheet",
    "Createur de planche d'image ronde",
    "A partir d'un dossier, on va generer une page avec des images rondes",
    "BACQUET Francis",
    "BACQUET Francis",
    "2014",
    "Planche images rondes",
    "",
    [
        (PF_SPINNER, "size", "taille de l'image en pixels", 100, (1, 3000, 1)),
        (PF_DIRNAME, "repertoire", "Dossier avec les images: ", "")
    ],
    [],
    picture_square_sheet, menu="<Image>/File/Create")

main()

