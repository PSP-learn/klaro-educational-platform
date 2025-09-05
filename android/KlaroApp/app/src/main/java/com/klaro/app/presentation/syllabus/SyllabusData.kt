package com.klaro.app.presentation.syllabus

object SyllabusData {
    private val classes = listOf("Class 9", "Class 10", "Class 11", "Class 12")
    private val subjects = listOf("Mathematics", "Physics", "Chemistry", "Biology")

    // NCERT-inspired topics and subtopics (simplified)
    private val data: Map<String, Map<String, Map<String, List<String>>>> = mapOf(
        "Class 11" to mapOf(
            "Mathematics" to mapOf(
                "Sets and Functions" to listOf("Sets", "Relations & Functions", "Trigonometric Functions"),
                "Algebra" to listOf("Complex Numbers", "Quadratic Equations", "Sequences & Series"),
                "Coordinate Geometry" to listOf("Straight Lines", "Conic Sections"),
                "Calculus" to listOf("Limits & Derivatives")
            ),
            "Physics" to mapOf(
                "Mechanics" to listOf("Units & Measurements", "Kinematics", "Laws of Motion", "Work, Energy & Power"),
                "Waves & Oscillations" to listOf("Oscillations", "Waves")
            ),
            "Chemistry" to mapOf(
                "Physical Chemistry" to listOf("Some Basic Concepts", "Atomic Structure", "Thermodynamics", "Equilibrium"),
                "Organic Chemistry" to listOf("Hydrocarbons", "Isomerism"),
                "Inorganic Chemistry" to listOf("s-Block Elements", "p-Block Elements")
            )
        ),
        "Class 12" to mapOf(
            "Mathematics" to mapOf(
                "Relations & Functions" to listOf("Inverse Trigonometric Functions"),
                "Algebra" to listOf("Matrices", "Determinants"),
                "Calculus" to listOf("Continuity & Differentiability", "Application of Derivatives", "Integrals", "Differential Equations"),
                "Vectors & 3D" to listOf("Vectors", "Three Dimensional Geometry")
            ),
            "Physics" to mapOf(
                "Electrostatics" to listOf("Electric Charges & Fields", "Electrostatic Potential & Capacitance"),
                "Current & Magnetism" to listOf("Current Electricity", "Moving Charges & Magnetism"),
                "Waves & Optics" to listOf("Ray Optics", "Wave Optics")
            ),
            "Chemistry" to mapOf(
                "Physical Chemistry" to listOf("Solid State", "Solutions", "Electrochemistry", "Chemical Kinetics"),
                "Organic Chemistry" to listOf("Haloalkanes & Haloarenes", "Alcohols, Phenols & Ethers", "Aldehydes, Ketones & Acids"),
                "Inorganic Chemistry" to listOf("p-Block Elements", "d & f Block Elements", "Coordination Compounds")
            )
        ),
        "Class 9" to mapOf(
            "Mathematics" to mapOf(
                "Number Systems" to listOf("Real Numbers"),
                "Algebra" to listOf("Polynomials", "Linear Equations"),
                "Geometry" to listOf("Triangles", "Quadrilaterals"),
                "Statistics" to listOf("Data Handling")
            ),
            "Physics" to mapOf(
                "Motion" to listOf("Motion in a Straight Line"),
                "Force & Laws" to listOf("Laws of Motion")
            ),
            "Chemistry" to mapOf(
                "Matter" to listOf("Matter in Our Surroundings")
            )
        ),
        "Class 10" to mapOf(
            "Mathematics" to mapOf(
                "Algebra" to listOf("Quadratic Equations", "Arithmetic Progressions"),
                "Trigonometry" to listOf("Trigonometric Ratios", "Applications of Trigonometry"),
                "Geometry" to listOf("Circles"),
                "Statistics & Probability" to listOf("Statistics", "Probability")
            ),
            "Physics" to mapOf(
                "Electricity" to listOf("Ohm's Law", "Series & Parallel"),
                "Light" to listOf("Reflection & Refraction")
            ),
            "Chemistry" to mapOf(
                "Chemical Reactions" to listOf("Chemical Equations"),
                "Metals & Non-metals" to listOf("Properties & Reactions")
            )
        )
    )

    fun getClasses(): List<String> = classes
    fun getSubjects(): List<String> = subjects

    fun getTopics(subject: String, classLevel: String): List<String> {
        val topics = data[classLevel]?.get(subject)?.keys?.toList().orEmpty()
        return listOf("All Topics") + topics
    }

    fun getSubtopics(subject: String, classLevel: String, topic: String): List<String> {
        if (topic == "All Topics") return listOf("All Subtopics")
        val subs = data[classLevel]?.get(subject)?.get(topic).orEmpty()
        return listOf("All Subtopics") + subs
    }
}

