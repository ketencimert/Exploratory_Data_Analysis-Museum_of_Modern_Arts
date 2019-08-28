library(datasets)
library(DT)
library(ggplot2)



art_shrunk = read.csv('art_shrunk.csv')
art_shrunk$Classification <- as.factor(art_shrunk$Classification)
#top_artists = c('Jackson Pollock', 'Barnett Newman', 'Mark Rothko', 'Vincent van Gogh','Helen Frankenthaler',
#'Agnes Martin','Joan Mitchell','Eva Hesse','Ruth Asawa','Yayoi Kusama','Grace Hartigan','Jean-Michel Basquiat','Marcel Duchamp')
#art_shrunk = art[art$Artist %in% top_artists, ]
#art_shrunk = subset(art_shrunk, art_shrunk$artist_age < 120)  
#art_shrunk = subset(art_shrunk, art_shrunk$artist_age > 0)  
#art_shrunk = subset(art_shrunk, art_shrunk$artist_age_acq < 100)
art_shrunk = art_shrunk[,c("Artist","Title","BeginDate", "EndDate", "Medium","Classification","URL","ThumbnailURL", "X0", "artist_age_acq", "artist_age", "artist_dead")]
colnames(art_shrunk)[colnames(art_shrunk) == 'X0'] <- 'Nationality'



art_shrunk$ThumbnailURL <- paste0("<a href='",art_shrunk$ThumbnailURL,"' target='_blank'>",'Picture',"</a>")
art_shrunk$URL <- paste0("<a href='",art_shrunk$URL,"' target='_blank'>",'More Info',"</a>")


world_phone = data.frame(WorldPhones)

# Define a server for the Shiny app
server = function(input, output) {
  
  # Fill in the spot we created for a plot
  output$phonePlot <- renderPlot({
    
    # Render a barplot
    ggplot(art_shrunk[art_shrunk$Artist %in% input$artist_name, ], aes(artist_age, artist_age_acq, colour = Classification)) + geom_point(size = 5) +
	xlab("Age at Beginning of Artwork") + 
	ylab("Acquisition by MOMA relative to date of death (positive = before death)") + ggtitle("Comparing Artists Age at Work and MOMA acquisition") + 
	theme(plot.title = element_text(hjust = 0.5))
  })
  
    output$click_info <- renderDataTable({
    # Because it's a ggplot2, we don't need to supply xvar or yvar; if this
    # were a base graphics plot, we'd need those.
    nearPoints(art_shrunk[art_shrunk$Artist %in% input$artist_name, ], input$plot1_click, addDist = TRUE)
  }, escape = FALSE)
  
    output$click_info2 <- renderText({
    # Because it's a ggplot2, we don't need to supply xvar or yvar; if this
    # were a base graphics plot, we'd need those.
    c('<img src="',unlist(strsplit(as.character(nearPoints(art_shrunk[art_shrunk$Artist %in% input$artist_name, ], input$plot1_click, addDist = TRUE)[8]), "'"))[2],'">')
  })
  
    

  output$brush_info <- renderDataTable({
    brushedPoints(art_shrunk[art_shrunk$Artist %in% input$artist_name, ], input$plot1_brush)
  }, escape = FALSE)
  
  
	output$picture<-renderText({paste0('<img src="',input$click_info2,'">')})
	
  
  
}



# Use a fluid Bootstrap layout
ui = fluidPage(    
  
  # Give the page a title
  titlePanel("A Look At Artist Productivity"),
  
  # Generate a row with a sidebar
  sidebarLayout(      
    
    # Define the sidebar with one input
    sidebarPanel(
      selectInput("artist_name", "Artist:", 
                  choices=unique(art_shrunk$Artist)),
      hr(),
      helpText("Data from data.world/moma")
    ),
    
    # Create a spot for the barplot
    mainPanel(
      plotOutput("phonePlot", click = "plot1_click",
        brush = brushOpts(
          id = "plot1_brush"
        ))  
    )
    
  ),
	fluidRow(
      h4("Artist's Work (Click a point to view work)"),
      htmlOutput("click_info2")
    ),  
    fluidRow(
      h4("Points near click"),
      dataTableOutput("click_info")
    ),
	fluidRow(
      h4("Brushed points"),
      dataTableOutput("brush_info")
    )

  
)

shinyApp(ui, server)
