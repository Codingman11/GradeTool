# GradeTool
# The tool for evaluating students' projects in various LUT programming courses.

# DEPENDENCIES
    pip install dearpygui

# Käyttöohje

    # Avaa GradingTool kansio Visual Studiossa
        Käynnistä ohjelma joko terminaalissa 
            Jos olet GradeTool pathissa: 
                python ./src/GradingTool.py
            Jos olet GradeTool/src pathissa:
                python GradingTool.py
        Tai  
            Avaa GradingTool.py ja suorita CTRL + F5 tai play nappulaa

    # Jos ikkuna näyttää liian pieneltä tai isolta niin voit säätää DEFAULT_WIDTH ja DEFAULT_FONT GradingTool.py:n alussa
       Defaulttina on
        DEFAULT_WIDTH = 1080
        DEFAULT_WIDTH = 23

    # KUSTOMOINTI
        - Voit säätää ikkunoiden leveyttä vetämällä ikkunan reunaa 
        - Voit siirtää ikkunan paikkaa pitämällä ikkunan nimen kohtaa ja siirtää miten haluat.
        
        Ohjelman päätyttyä käyttöliittymä tallentuu 
     
    # Opiskelija ikkuna (Oikealla ylhäällä)
        Valitaan opiskelija

    # Arviointitaulukko (Opiskelija ikkunan alapuolella)
        Merkkaa opiskelijanumero input kohtaan

    # Palautteet ikkuna (Arviointitaulukko ikkunan alla)
        ON KÄYTÖSSÄ > v 0.2.1
        Voit muokata kommenttia tällä hetkellä yhdellä rivillä.

    # "Kirjoita tiedostoihin" nappi(Opiskelija ikkunan listan yläpuolella)
        Ennen kuin lopetat ohjelman MUISTA kirjoittaa tiedostoihin,
        niin data tallentuu muuten joudut laittamaan virheet uudestaan 
