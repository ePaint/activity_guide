# Generated by Django 4.2.7 on 2023-12-18 22:26

from django.db import migrations


class Migration(migrations.Migration):

    # Creates 20 basic activities per category (Sports, Art, and Science)
    def custom_task(self, schema_editor):
        to_create = [
            # 20 Sports activities
            {
                "name": "Soccer",
                "description": "Global team sport played with a ball and feet, aiming to score goals in the opponent's net.",
                "category": "sports",
                "slugName": "soccer"
            },
            {
                "name": "Basketball",
                "description": "Fast-paced team sport where players shoot a ball through the opponent's hoop to score points.",
                "category": "sports",
                "slugName": "basketball"
            },
            {
                "name": "Swimming",
                "description": "Individual or team aquatic sport where participants move through water using various strokes.",
                "category": "sports",
                "slugName": "swimming"
            },
            {
                "name": "Tennis",
                "description": "Racket sport played between two opponents or teams, involving hitting a ball over a net.",
                "category": "sports",
                "slugName": "tennis"
            },
            {
                "name": "Volleyball",
                "description": "Team sport played with a ball over a net, aiming to score points by grounding the ball in the opponent's court.",
                "category": "sports",
                "slugName": "volleyball"
            },
            {
                "name": "Ice Hockey",
                "description": "Fast-paced team sport played on ice, where players use sticks to score goals by shooting a puck into the opponent's net.",
                "category": "sports",
                "slugName": "ice-hockey"
            },
            {
                "name": "Baseball",
                "description": "Bat-and-ball sport played between two teams, aiming to score runs by hitting a pitched ball and running around bases.",
                "category": "sports",
                "slugName": "baseball"
            },
            {
                "name": "Table Tennis",
                "description": "Indoor racket sport played with a lightweight ball, requiring quick reflexes and precise shots over a table.",
                "category": "sports",
                "slugName": "table-tennis"
            },
            {
                "name": "Golf",
                "description": "Precision sport where players use clubs to hit a ball into a series of holes on a course with the fewest strokes.",
                "category": "sports",
                "slugName": "golf"
            },
            {
                "name": "Running",
                "description": "Individual or team activity involving rapid movement on foot over varying distances, often in races.",
                "category": "sports",
                "slugName": "running"
            },
            {
                "name": "Cycling",
                "description": "Sport and recreational activity involving riding bicycles, promoting physical fitness and outdoor exploration.",
                "category": "sports",
                "slugName": "cycling"
            },
            {
                "name": "Martial Arts",
                "description": "Various disciplines of combat training and techniques, often practiced for self-defense, fitness, and discipline.",
                "category": "sports",
                "slugName": "martial-arts"
            },
            {
                "name": "Badminton",
                "description": "Racket sport played with a shuttlecock, aiming to score points by hitting it over a net into the opponent's side.",
                "category": "sports",
                "slugName": "badminton"
            },
            {
                "name": "Gymnastics",
                "description": "Sport involving physical exercises requiring strength, flexibility, balance, and control, often performed on apparatus or in routines.",
                "category": "sports",
                "slugName": "gymnastics"
            },
            {
                "name": "Skiing",
                "description": "Winter sport involving sliding on snow using skis, with various disciplines such as alpine, cross-country, and freestyle.",
                "category": "sports",
                "slugName": "skiing"
            },
            {
                "name": "Surfing",
                "description": "Water sport where participants ride waves on a board, balancing and maneuvering in the ocean.",
                "category": "sports",
                "slugName": "surfing"
            },
            {
                "name": "Archery",
                "description": "Skill-based sport involving using a bow to shoot arrows at a target, emphasizing precision and focus.",
                "category": "sports",
                "slugName": "archery"
            },
            {
                "name": "Rock Climbing",
                "description": "Activity involving ascending natural or artificial rock formations, requiring strength, technique, and mental focus.",
                "category": "sports",
                "slugName": "rock-climbing"
            },
            {
                "name": "Wrestling",
                "description": "Combat sport involving grappling techniques to throw or pin opponents, emphasizing strength, strategy, and agility.",
                "category": "sports",
                "slugName": "wrestling"
            },
            {
                "name": "Sailing",
                "description": "Water sport involving controlling a sailboat, harnessing wind power to navigate across bodies of water.",
                "category": "sports",
                "slugName": "sailing"
            },
            
            # 20 Art activities
            {
                "name": "Painting",
                "description": "Visual art form involving the application of pigments to a surface, expressing creativity and emotion.",
                "category": "art",
                "slugName": "painting"
            },
            {
                "name": "Dancing",
                "description": "Expressive movement to music, encompassing various styles and cultural forms of artistic dance.",
                "category": "art",
                "slugName": "dancing"
            },
            {
                "name": "Photography",
                "description": "Artistic practice of capturing and creating images using a camera, exploring visual storytelling.",
                "category": "art",
                "slugName": "photography"
            },
            {
                "name": "Sculpture",
                "description": "Artistic practice of creating three-dimensional forms using materials such as clay, metal, or stone.",
                "category": "art",
                "slugName": "sculpture"
            },
            {
                "name": "Music Composition",
                "description": "Creative process of writing and arranging musical pieces, exploring harmony, melody, and rhythm.",
                "category": "art",
                "slugName": "music-composition"
            },
            {
                "name": "Drawing",
                "description": "Visual art form using various tools to create images on paper or other surfaces, exploring lines, shapes, and shading.",
                "category": "art",
                "slugName": "drawing"
            },
            {
                "name": "Digital Art",
                "description": "Artistic creation using digital tools and technology, exploring new media and visual expressions.",
                "category": "art",
                "slugName": "digital-art"
            },
            {
                "name": "Theater Acting",
                "description": "Performing in stage productions, bringing characters to life through dialogue, movement, and expression.",
                "category": "art",
                "slugName": "theater-acting"
            },
            {
                "name": "Film Making",
                "description": "Creative process of producing visual stories through filmmaking, involving scripting, directing, and editing.",
                "category": "art",
                "slugName": "film-making"
            },
            {
                "name": "Ceramics",
                "description": "Art and craft of creating objects from clay, often shaped on a potter's wheel and fired in a kiln.",
                "category": "art",
                "slugName": "ceramics"
            },
            {
                "name": "Fashion Design",
                "description": "Art and practice of creating clothing and accessories, exploring style, fabric, and design aesthetics.",
                "category": "art",
                "slugName": "fashion-design"
            },
            {
                "name": "Graphic Design",
                "description": "Visual communication through the use of images, typography, and layout, often for print or digital media.",
                "category": "art",
                "slugName": "graphic-design"
            },
            {
                "name": "Poetry Writing",
                "description": "Artistic expression through the written word, exploring rhythm, imagery, and emotion in poetic form.",
                "category": "art",
                "slugName": "poetry-writing"
            },
            {
                "name": "Mural Painting",
                "description": "Large-scale visual art created on walls or surfaces, often reflecting cultural, social, or political themes.",
                "category": "art",
                "slugName": "mural-painting"
            },
            {
                "name": "Jewelry Making",
                "description": "Craft of creating wearable art, often using metals, gemstones, and other materials to design unique pieces.",
                "category": "art",
                "slugName": "jewelry-making"
            },
            {
                "name": "Printmaking",
                "description": "Artistic technique involving the creation of images on surfaces for reproduction, such as etching or linocut.",
                "category": "art",
                "slugName": "printmaking"
            },
            {
                "name": "Calligraphy",
                "description": "Art of beautiful handwriting, often emphasizing decorative lettering styles, shapes, and flourishes.",
                "category": "art",
                "slugName": "calligraphy"
            },
            {
                "name": "Collage Art",
                "description": "Artistic composition created by assembling various materials, such as paper, fabric, or found objects, into a unified whole.",
                "category": "art",
                "slugName": "collage-art"
            },
            {
                "name": "Stand-up Comedy",
                "description": "Performance art involving a comedian presenting humorous stories, jokes, and observations to entertain an audience.",
                "category": "art",
                "slugName": "stand-up-comedy"
            },
            {
                "name": "Pottery",
                "description": "Art and craft of creating objects from clay, often shaped on a potter's wheel and fired in a kiln.",
                "category": "art",
                "slugName": "pottery"
            },

            # 20 Science activities
            {
                "name": "Chemistry Experiments",
                "description": "Engaging in hands-on experiments to explore chemical reactions and principles.",
                "category": "science",
                "slugName": "chemistry-experiments"
            },
            {
                "name": "Astronomy Observation",
                "description": "Studying celestial objects and phenomena through telescopes and observations.",
                "category": "science",
                "slugName": "astronomy-observation"
            },
            {
                "name": "Botany Study",
                "description": "Exploring plant life, anatomy, and growth patterns to understand the world of plants.",
                "category": "science",
                "slugName": "botany-study"
            },
            {
                "name": "Physics Experiments",
                "description": "Engaging in experiments to explore physical principles and phenomena, involving measurements and observations.",
                "category": "science",
                "slugName": "physics-experiments"
            },
            {
                "name": "Ecology Research",
                "description": "Study of the relationships between living organisms and their environment, exploring ecosystems and biodiversity.",
                "category": "science",
                "slugName": "ecology-research"
            },
            {
                "name": "Geology Exploration",
                "description": "Investigating Earth's structure, composition, and processes through the study of rocks, minerals, and landscapes.",
                "category": "science",
                "slugName": "geology-exploration"
            },
            {
                "name": "Zoology Observation",
                "description": "Observing and studying animals to understand their behavior, physiology, and ecological roles.",
                "category": "science",
                "slugName": "zoology-observation"
            },
            {
                "name": "Meteorology Experiments",
                "description": "Conducting experiments to explore atmospheric phenomena, weather patterns, and climate science.",
                "category": "science",
                "slugName": "meteorology-experiments"
            },
            {
                "name": "Microbiology Research",
                "description": "Studying microscopic organisms, including bacteria, viruses, and fungi, to understand their biology and impact.",
                "category": "science",
                "slugName": "microbiology-research"
            },
            {
                "name": "Genetics Analysis",
                "description": "Exploring genetic principles, inheritance patterns, and DNA structure through experimental analysis.",
                "category": "science",
                "slugName": "genetics-analysis"
            },
            {
                "name": "Chemical Engineering",
                "description": "Applying chemical principles to design and optimize processes for the production of chemicals and materials.",
                "category": "science",
                "slugName": "chemical-engineering"
            },
            {
                "name": "Astrophysics Research",
                "description": "Conducting theoretical and observational studies to understand the physical properties and behavior of celestial bodies.",
                "category": "science",
                "slugName": "astrophysics-research"
            },
            {
                "name": "Environmental Monitoring",
                "description": "Collecting and analyzing data to assess the impact of human activities on the environment and ecosystems.",
                "category": "science",
                "slugName": "environmental-monitoring"
            },
            {
                "name": "Neuroscience Investigations",
                "description": "Studying the nervous system, including the brain and nervous tissue, to understand cognitive and physiological processes.",
                "category": "science",
                "slugName": "neuroscience-investigations"
            },
            {
                "name": "Materials Science Experiments",
                "description": "Exploring the properties and applications of materials, including metals, polymers, and composites.",
                "category": "science",
                "slugName": "materials-science-experiments"
            },
            {
                "name": "Renewable Energy Projects",
                "description": "Designing and implementing projects to harness renewable energy sources, such as solar, wind, and hydro power.",
                "category": "science",
                "slugName": "renewable-energy-projects"
            },
            {
                "name": "Astrobiology Research",
                "description": "Exploring the potential for life beyond Earth and studying extreme environments as analogs for extraterrestrial habitats.",
                "category": "science",
                "slugName": "astrobiology-research"
            },
            {
                "name": "Mathematics Investigations",
                "description": "Exploring mathematical theories, theorems, and applications through analytical and computational methods.",
                "category": "science",
                "slugName": "mathematics-investigations"
            },
            {
                "name": "Nuclear Physics Experiments",
                "description": "Conducting experiments to study the behavior and properties of atomic nuclei, including nuclear reactions.",
                "category": "science",
                "slugName": "nuclear-physics-experiments"
            },
            {
                "name": "Oceanography Studies",
                "description": "Investigating the physical, chemical, and biological properties of the oceans, including marine life and ecosystems.",
                "category": "science",
                "slugName": "oceanography-studies"
            }
        ]

        Activity = self.get_model('activities', 'Activity')
        Category = self.get_model('categories', 'Category')
        
        for item in to_create:
            category = Category.objects.get(slug=item['category'])
            Activity.objects.get_or_create(
                name=item['name'],
                description=item['description'],
                category=category,
                slug=item['slugName']
            )

    dependencies = [
        ('activities', '0002_alter_activity_options'),
    ]

    operations = [
        migrations.RunPython(custom_task, migrations.RunPython.noop),
    ]
