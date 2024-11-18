# Import necessary libraries
import seaborn as sns  # For data visualization (scatterplot)
from faicons import icon_svg  # For rendering icons
from shiny import reactive  # For reactivity in the app
from shiny.express import input, render, ui  # UI components, input handling, and rendering
import palmerpenguins  # Dataset with penguin data

# Load the penguin dataset into a DataFrame
df = palmerpenguins.load_penguins()

# Set the options for the page (title, favicon, etc.)
ui.page_opts(
    title="Penguins Dashboard - Explore the Penguin Species",  # Page title
    fillable=True,  # Make the page fillable
    favicon="favicon.ico"  # Reference the favicon
)


# Define the sidebar layout for the filter controls
with ui.sidebar(title="Penguin Filters"):
    # Slider input for selecting the maximum mass (body mass in grams)
    ui.input_slider("mass", "Select Maximum Mass (grams)", 2000, 6000, 6000)
    
    # Checkbox group for selecting the species of penguins to filter by
    ui.input_checkbox_group(
        "species",  # ID for this input
        "Choose Species",  # Label for the input
        ["Adelie", "Gentoo", "Chinstrap"],  # Options for species
        selected=["Adelie", "Gentoo", "Chinstrap"],  # Default selected species
    )
    
    # Horizontal rule for separating sections
    ui.hr()
    
    # Display some external links for additional resources
    ui.h6("Learn More")
    ui.a(
        "GitHub Source Code",  # Text for the link
        href="https://github.com/denisecase/cintel-07-tdash",  # URL to the GitHub repository
        target="_blank",  # Open the link in a new tab
    )
    ui.a("Explore the App", href="https://denisecase.github.io/cintel-07-tdash/", target="_blank")
    ui.a("GitHub Issues", href="https://github.com/denisecase/cintel-07-tdash/issues", target="_blank")
    ui.a("About PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a("Dashboard Template", href="https://shiny.posit.co/py/templates/dashboard/", target="_blank")
    ui.a("More Projects", href="https://github.com/denisecase/pyshiny-penguins-dashboard-express", target="_blank")

# Define the main layout using columns and value boxes to show key metrics
with ui.layout_column_wrap():
    # Value box showing the number of penguins in the filtered dataset
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Penguin Count"  # Title of the value box

        # Render the count of penguins (rows in the filtered DataFrame)
        @render.text
        def count():
            return f"{filtered_df().shape[0]} penguins"  # Add the unit (penguins)

    # Value box showing the average bill length of the selected species
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average Bill Length"  # Title of the value box

        # Render the average bill length from the filtered data
        @render.text
        def bill_length():
            return f"Avg: {filtered_df()['bill_length_mm'].mean():.1f} mm"  # Show the value and unit (mm)

    # Value box showing the average bill depth of the selected species
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average Bill Depth"  # Title of the value box

        # Render the average bill depth from the filtered data
        @render.text
        def bill_depth():
            return f"Avg: {filtered_df()['bill_depth_mm'].mean():.1f} mm"  # Show the value and unit (mm)

# Define a section with multiple cards (one for the plot and one for the data grid)
with ui.layout_columns():
    # Card for displaying the scatterplot of bill length vs. bill depth
    with ui.card(full_screen=True):
        ui.card_header("Bill Length vs Bill Depth")  # Updated card header

        # Render the scatterplot based on the filtered data
        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),  # Use the filtered data
                x="bill_length_mm",  # x-axis: bill length
                y="bill_depth_mm",  # y-axis: bill depth
                hue="species",  # Hue (color) based on species
            )

    # Card for displaying the summary statistics of the dataset
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data Overview")  # Updated card header

        # Render the summary statistics in a data grid (showing a subset of columns)
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",  # Species of the penguin
                "island",  # Island where the penguin was found
                "bill_length_mm",  # Bill length in millimeters
                "bill_depth_mm",  # Bill depth in millimeters
                "body_mass_g",  # Body mass in grams
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)  # Render the DataGrid with filters
            

# Define the reactive calculation that filters the DataFrame based on user input
@reactive.calc
def filtered_df():
    # Filter the penguins dataset by selected species
    filt_df = df[df["species"].isin(input.species())]
    
    # Further filter the data based on the selected body mass
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    
    return filt_df  # Return the filtered DataFrame
