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

    # Jos ikkuna näyttää liian isolta niin voit säätää DEFAULT_WIDTH ja FONT_SCALE GradingTool.py:n alussa
       Defaulttina on
        DEFAULT_WIDTH = 900
        FONT_SCALE = 1.2

    # KUSTOMOINTI
        - Voit säätää ikkunoiden leveyttä vetämällä ikkunan reunaa 
        - Voit siirtää ikkunan paikkaa pitämällä ikkunan nimen kohtaa ja siirtää miten haluat.
        
        Ohjelman päätyttyä käyttöliittymä tallentuu 
     
    # Opiskelija ikkuna (Oikealla ylhäällä)
        Valitaan opiskelija

    # Arviointitaulukko (Opiskelija ikkunan alapuolella)
        Merkkaa opiskelijanumero input kohtaan

    # Feedback ikkuna (Arviointitaulukko ikkunan alla)
        EI OLE KÄYTÖSSÄ

    # "Kirjoita tiedostoihin" nappi(Opiskelija ikkunan listan yläpuolella)
        Ennen kuin lopetat ohjelman MUISTA kirjoittaa tiedostoihin,
        niin data tallentuu muuten joudut laittamaan virheet uudestaan 
