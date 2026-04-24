/* ===================================================
   HENDSETNA | هندستنا — script.js
   =================================================== */

/* ============================================================
   TRANSLATION DATA
   ============================================================ */
const translations = {
  en: {
    nav_home: "Home",
    nav_how: "How It Works",
    nav_start: "Start Design",
    nav_results: "Results",
    cta_btn: "Start New Design",
    demo_btn: "View Demo Result",
    hero_badge: "✦ AI-Powered Design",
    hero_headline: "AI Interior Design Assistant for Creative Designers",
    hero_sub:
      "Transform client preferences, space details, colors, materials, furniture choices, and visual inspirations into a complete interior design concept with a suggested AI-generated image.",
    badge1: "✦ Gemini-powered",
    badge2: "Design Brief",
    badge3: "AI Image Prompt",
    badge4: "Client-ready Concept",
    hero_img_placeholder: "Interior Design Preview",
    overlay_label: "Suggested Design Preview",
    style_label: "Style",
    mood_label: "Mood",
    hero_mood: "Warm & Creative",
    palette_label: "Palette",

    how_eyebrow: "The Process",
    how_title: "How Hendsetna Works",
    step1_title: "Choose Project Type",
    step1_desc:
      "Select whether the space is residential, commercial, administrative, or hospitality.",
    step2_title: "Enter Space Details",
    step2_desc:
      "Add dimensions, area, ceiling height, budget, current condition, and user needs.",
    step3_title: "Add Preferences & Inspiration",
    step3_desc:
      "Choose style, colors, materials, lighting, furniture, and upload logos or reference images.",
    step4_title: "Generate Design Concept",
    step4_desc:
      "Get a design brief, visual direction, image prompt, and suggested design preview.",

    types_eyebrow: "Step 1",
    types_title: "Choose Your Project Type",
    types_sub:
      "Select the type of space you want to design so Hendsetna can ask the right questions.",
    type_res: "Residential",
    type_res_desc:
      "Homes, apartments, villas, bedrooms, living rooms, kitchens, and family spaces.",
    type_com: "Commercial",
    type_com_desc:
      "Cafés, restaurants, stores, clinics, salons, showrooms, and customer-facing spaces.",
    type_adm: "Administrative",
    type_adm_desc:
      "Offices, meeting rooms, reception areas, workspaces, manager rooms, and training rooms.",
    type_hos: "Hospitality / Tourism",
    type_hos_desc:
      "Hotel rooms, resort lobbies, guest houses, lounges, chalets, and tourism spaces.",
    choose_btn: "Choose this type",

    back_btn: "Back to Project Types",
    generate_btn: "✦ Generate Design Concept",

    basics_title: "Project Basics",
    proj_name: "Project Name",
    space_type: "Space Type",
    select_placeholder: "— Select —",
    sp_bedroom: "Bedroom",
    sp_living: "Living Room",
    sp_kitchen: "Kitchen",
    sp_bathroom: "Bathroom",
    sp_dining: "Dining Room",
    sp_kids: "Kids Room",
    sp_balcony: "Balcony",
    sp_apartment: "Full Apartment",
    sp_villa: "Villa",
    sp_office: "Office Room",
    sp_meeting: "Meeting Room",
    sp_reception: "Reception Area",
    sp_openwork: "Open Workspace",
    sp_manager: "Manager Room",
    sp_training: "Training Room",
    sp_hotel: "Hotel Room",
    sp_lobby: "Resort Lobby",
    sp_guesthouse: "Guest House",
    sp_lounge: "Lounge",
    sp_chalet: "Chalet",
    sp_restaurant_area: "Restaurant Area",

    area_label: "Area (m²)",
    dimensions_label: "Dimensions",
    ceiling_label: "Ceiling Height (m)",
    users_label: "Number of Users",
    condition_label: "Current Condition",
    cond_empty: "Empty Space",
    cond_reno: "Renovation",
    cond_furnished: "Already Furnished",
    cond_construction: "Under Construction",

    style_pref_title: "Style Preferences",
    int_style: "Interior Style",
    style_suggest: "Not sure, suggest one",
    style_bold: "Bold & Creative",
    style_brand: "Brand-focused",
    style_resort: "Resort Style",
    style_modern_luxury: "Modern Luxury",
    style_arabic_luxury: "Arabic Luxury",
    custom_style: "Custom Style Description",
    mood_family: "Family-friendly",

    colors_title: "Colors",
    pref_colors: "Preferred Colors",
    avoid_colors: "Colors to Avoid",

    materials_title: "Materials",
    mat_wood: "Wood",
    mat_marble: "Marble",
    mat_glass: "Glass",
    mat_metal: "Metal",
    mat_concrete: "Concrete",
    mat_fabric: "Fabric",
    mat_leather: "Leather",
    mat_velvet: "Velvet",
    mat_ceramic: "Ceramic",
    mat_stone: "Natural Stone",
    mat_rattan: "Rattan",
    mat_mirror: "Mirror",

    furniture_title: "Furniture",
    furniture_req: "Furniture Requirements",
    furniture_placeholder:
      "Example: one bed only, small desk near the window, large wardrobe, no TV unit.",

    lighting_title: "Lighting",
    light_purpose: "Main Lighting Purpose",
    light_purpose_ph: "— Select purpose —",
    light_functional: "Functional Lighting",
    light_mood: "Mood Lighting",
    light_decorative: "Decorative Lighting",
    light_display: "Display Lighting",
    light_relaxing: "Relaxing Lighting",
    light_work: "Work-focused Lighting",
    light_natural: "Natural Light",
    light_natural_ph: "— Select natural light —",
    light_strong: "Strong Natural Light",
    light_medium: "Medium Natural Light",
    light_weak: "Weak Natural Light",
    light_none: "No Natural Light",
    light_temp: "Preferred Lighting Temperature",
    light_temp_ph: "— Select temperature —",
    light_warm: "Warm Lighting",
    light_neutral: "Neutral Lighting",
    light_cool: "Cool White Lighting",
    light_fixtures: "Lighting Fixtures",
    light_fixture_note: "Choose only the fixtures suitable for the space.",
    light_led: "Hidden LED Lighting",
    light_spot: "Spotlights",
    light_pendant: "Pendant Lights",
    light_chandelier: "Chandeliers",
    light_sconce: "Wall Sconces",
    light_floor: "Floor Lamps",
    light_table: "Table Lamps",
    light_track: "Track Lighting",
    light_hint:
      "Hendsetna will recommend the most suitable lighting combination based on the space type and mood.",

    inspiration_title: "Personal Inspiration",
    inspiration_label: "Describe Inspiration",
    uploads_title: "Reference Images",
    upload_room: "Room Image",
    upload_room_desc: "Upload current state of the space",
    upload_inspo: "Inspiration Image",
    upload_inspo_desc: "Share visual references or style examples",
    upload_mood: "Moodboard",
    upload_mood_desc: "Upload a compiled moodboard if available",
    upload_logo: "Brand Logo",
    upload_logo_desc: "Upload your brand logo or visual identity",
    upload_ref: "Reference Design",
    upload_ref_desc: "Upload reference spaces you admire",
    upload_logo_co: "Company Logo",
    upload_logo_co_desc: "Upload your company logo or brand guide",
    choose_image: "Choose Image",
    upload_note: "Image analysis will be connected later.",

    business_type: "Business Type",
    brand_name: "Brand Name",
    brand_colors: "Brand Colors",
    target_customers: "Target Customers",
    zones_title: "Required Zones",
    zone_reception: "Reception",
    zone_waiting: "Waiting Area",
    zone_display: "Display Area",
    zone_seating: "Seating Area",
    zone_cashier: "Cashier",
    zone_storage: "Storage",
    zone_photo: "Photo Spot",
    zone_desks: "Desks",
    zone_meeting: "Meeting Table",
    zone_waiting_seats: "Waiting Seats",
    zone_presentation: "Presentation Screen",
    zone_coffee: "Coffee Corner",

    company_label: "Company / Organization",
    employees_label: "Number of Employees / Users",
    work_style_title: "Work Style",
    work_style_label: "Office Style",

    guest_type: "Target Guest Type",
    guest_business: "Business Travelers",
    guest_luxury: "Luxury Guests",

    notes_title: "Additional Notes",

    res_form_title: "Residential Design Details",
    res_form_sub: "Tell Hendsetna about the home space you want to design.",
    com_form_title: "Commercial Design Details",
    com_form_sub: "Tell Hendsetna about your commercial space requirements.",
    adm_form_title: "Administrative Design Details",
    adm_form_sub: "Tell Hendsetna about your workspace requirements.",
    hos_form_title: "Hospitality / Tourism Design Details",
    hos_form_sub: "Tell Hendsetna about your hospitality space requirements.",

    results_eyebrow: "Design Concept Ready",
    results_title: "Generated Design Concept",
    result_img_label: "Suggested AI Design Image",
    result_img_note: "Image generation will appear here after API integration.",
    design_summary: "Design Summary",
    sum_type: "Project Type",
    sum_style: "Style Direction",
    sum_mood: "Mood",
    sum_mood_val: "Calm, warm, functional",
    sum_palette: "Color Palette",
    sum_materials: "Materials",
    sum_materials_val: "Natural wood · Linen · Matte ceramic",
    sum_lighting: "Lighting",
    sum_lighting_val: "Warm hidden LED + Pendant lights",
    sum_furniture: "Furniture",
    sum_furniture_val: "One bed · Compact desk · Large wardrobe",
    res_brief_title: "Design Brief",
    res_brief_body:
      "The space will be designed with a calm modern direction, focusing on functionality, visual harmony, warm lighting, and materials that match the client's lifestyle and preferences.",
    res_palette_title: "Color Palette",
    res_materials_title: "Materials",
    res_materials_list: null,
    res_furniture_title: "Furniture Suggestions",
    res_furniture_list: null,
    res_lighting_title: "Lighting Suggestions",
    res_lighting_list: null,
    res_prompt_title: "Image Generation Prompt",
    res_prompt_body:
      "Create a realistic interior design render of a calm Japandi-style bedroom. Natural oak wood flooring, linen curtains, warm hidden LED ceiling coves, a low platform bed, compact floating desk near the window, integrated wardrobe with brushed brass handles. Color palette: beige, off-white, warm wood tones, olive green accents. Soft warm 2700K lighting. Photorealistic, professional interior photography style.",
    copy_btn: "Copy Prompt",
    edit_btn: "Edit Requirements",
    new_design_btn: "+ Start New Design",
    pdf_btn: "⬇ Download Concept PDF",
    footer_tagline:
      "AI-powered interior design assistant for creative professionals.",
    footer_copy:
      "© 2025 Hendsetna. Built for interior designers, decor engineers & architects.",
  },

  ar: {
    nav_home: "الرئيسية",
    nav_how: "كيف يعمل",
    nav_start: "ابدأ التصميم",
    nav_results: "النتائج",
    cta_btn: "ابدأ تصميم جديد",
    demo_btn: "عرض نتيجة تجريبية",
    hero_badge: "✦ مدعوم بالذكاء الاصطناعي",
    hero_headline: "مساعد ذكي لمهندسي الديكور والتصميم الداخلي",
    hero_sub:
      "حوّل تفاصيل المكان وذوق العميل والألوان والخامات والصور المرجعية إلى تصور تصميمي كامل وصورة مقترحة للتصميم.",
    badge1: "✦ مدعوم بـ Gemini",
    badge2: "ملخص تصميم",
    badge3: "برومبت الصورة",
    badge4: "مفهوم جاهز للعميل",
    hero_img_placeholder: "معاينة التصميم الداخلي",
    overlay_label: "معاينة التصميم المقترح",
    style_label: "الأسلوب",
    mood_label: "الجو العام",
    hero_mood: "دافئ وإبداعي",
    palette_label: "لوحة الألوان",

    how_eyebrow: "طريقة العمل",
    how_title: "كيف تعمل هندستنا",
    step1_title: "اختر نوع المشروع",
    step1_desc:
      "حدد ما إذا كان المكان سكنياً أو تجارياً أو إدارياً أو سياحياً.",
    step2_title: "أدخل تفاصيل المساحة",
    step2_desc:
      "أضف الأبعاد والمساحة وارتفاع السقف والميزانية والحالة الحالية واحتياجات المستخدمين.",
    step3_title: "أضف التفضيلات والإلهام",
    step3_desc:
      "اختر الأسلوب والألوان والخامات والإضاءة والأثاث وقم بتحميل الشعارات أو الصور المرجعية.",
    step4_title: "ولّد مفهوم التصميم",
    step4_desc:
      "احصل على ملخص التصميم والتوجه البصري وبرومبت الصورة ومعاينة التصميم المقترح.",

    types_eyebrow: "الخطوة الأولى",
    types_title: "اختر نوع مشروعك",
    types_sub:
      "حدد نوع المساحة التي تريد تصميمها حتى تطرح هندستنا الأسئلة المناسبة.",
    type_res: "منزل",
    type_res_desc: "منازل وشقق وفلل وغرف نوم وغرف معيشة ومطابخ ومساحات عائلية.",
    type_com: "مكان تجاري",
    type_com_desc:
      "مقاهٍ ومطاعم ومحلات وعيادات وصالونات ومعارض ومساحات للعملاء.",
    type_adm: "مكان إداري",
    type_adm_desc:
      "مكاتب وغرف اجتماعات ومناطق استقبال ومساحات عمل وغرف مديرين وقاعات تدريب.",
    type_hos: "مكان سياحي / فندقي",
    type_hos_desc:
      "غرف فندقية وردهات منتجعات وبيوت ضيافة وصالات استرخاء وشاليهات ومساحات سياحية.",
    choose_btn: "اختر هذا النوع",

    back_btn: "العودة إلى أنواع المشاريع",
    generate_btn: "✦ ولّد مفهوم التصميم",

    basics_title: "أساسيات المشروع",
    proj_name: "اسم المشروع",
    space_type: "نوع المساحة",
    select_placeholder: "— اختر —",
    sp_bedroom: "غرفة نوم",
    sp_living: "غرفة معيشة",
    sp_kitchen: "مطبخ",
    sp_bathroom: "حمام",
    sp_dining: "غرفة طعام",
    sp_kids: "غرفة أطفال",
    sp_balcony: "شرفة",
    sp_apartment: "شقة كاملة",
    sp_villa: "فيلا",
    sp_office: "غرفة مكتب",
    sp_meeting: "غرفة اجتماعات",
    sp_reception: "منطقة الاستقبال",
    sp_openwork: "مساحة عمل مفتوحة",
    sp_manager: "غرفة المدير",
    sp_training: "قاعة تدريب",
    sp_hotel: "غرفة فندقية",
    sp_lobby: "ردهة منتجع",
    sp_guesthouse: "بيت ضيافة",
    sp_lounge: "صالة استرخاء",
    sp_chalet: "شاليه",
    sp_restaurant_area: "منطقة مطعم",

    area_label: "المساحة (م²)",
    dimensions_label: "الأبعاد",
    ceiling_label: "ارتفاع السقف (م)",
    users_label: "عدد المستخدمين",
    condition_label: "الحالة الحالية",
    cond_empty: "مساحة فارغة",
    cond_reno: "تجديد",
    cond_furnished: "مفروش بالفعل",
    cond_construction: "قيد الإنشاء",

    style_pref_title: "تفضيلات الأسلوب",
    int_style: "أسلوب التصميم الداخلي",
    style_suggest: "غير متأكد، اقترح لي",
    style_bold: "جريء وإبداعي",
    style_brand: "مرتكز على الهوية",
    style_resort: "أسلوب المنتجع",
    style_modern_luxury: "فاخر عصري",
    style_arabic_luxury: "فاخر عربي",
    custom_style: "وصف الأسلوب المخصص",
    mood_family: "مناسب للعائلة",

    colors_title: "الألوان",
    pref_colors: "الألوان المفضلة",
    avoid_colors: "ألوان يجب تجنبها",

    materials_title: "الخامات",
    mat_wood: "خشب",
    mat_marble: "رخام",
    mat_glass: "زجاج",
    mat_metal: "معدن",
    mat_concrete: "خرسانة",
    mat_fabric: "قماش",
    mat_leather: "جلد",
    mat_velvet: "مخمل",
    mat_ceramic: "سيراميك",
    mat_stone: "حجر طبيعي",
    mat_rattan: "روطان",
    mat_mirror: "مرايا",

    furniture_title: "الأثاث",
    furniture_req: "متطلبات الأثاث",
    furniture_placeholder:
      "مثال: سرير واحد فقط، مكتب صغير بالقرب من النافذة، خزانة كبيرة، بدون وحدة تلفزيون.",

    lighting_title: "الإضاءة",
    light_purpose: "الغرض الأساسي من الإضاءة",
    light_purpose_ph: "— اختر الغرض —",
    light_functional: "إضاءة وظيفية",
    light_mood: "إضاءة للأجواء",
    light_decorative: "إضاءة زخرفية",
    light_display: "إضاءة عرض",
    light_relaxing: "إضاءة للاسترخاء",
    light_work: "إضاءة للعمل",
    light_natural: "الضوء الطبيعي",
    light_natural_ph: "— اختر مستوى الضوء الطبيعي —",
    light_strong: "ضوء طبيعي قوي",
    light_medium: "ضوء طبيعي متوسط",
    light_weak: "ضوء طبيعي ضعيف",
    light_none: "لا يوجد ضوء طبيعي",
    light_temp: "درجة حرارة الإضاءة المفضلة",
    light_temp_ph: "— اختر درجة الحرارة —",
    light_warm: "إضاءة دافئة",
    light_neutral: "إضاءة محايدة",
    light_cool: "إضاءة بيضاء باردة",
    light_fixtures: "تجهيزات الإضاءة",
    light_fixture_note: "اختر فقط التجهيزات المناسبة للمساحة.",
    light_led: "إضاءة LED مخفية",
    light_spot: "سبوتات",
    light_pendant: "إضاءة معلقة",
    light_chandelier: "ثريات",
    light_sconce: "أباجورات جدارية",
    light_floor: "مصابيح أرضية",
    light_table: "مصابيح طاولة",
    light_track: "إضاءة مسارات",
    light_hint:
      "ستوصي هندستنا بأنسب مجموعة إضاءة بناءً على نوع المساحة والأجواء المطلوبة.",

    inspiration_title: "الإلهام الشخصي",
    inspiration_label: "صف الإلهام",
    uploads_title: "الصور المرجعية",
    upload_room: "صورة الغرفة",
    upload_room_desc: "حمّل الحالة الحالية للمساحة",
    upload_inspo: "صورة الإلهام",
    upload_inspo_desc: "شارك مراجع بصرية أو أمثلة أسلوب",
    upload_mood: "لوحة المزاج",
    upload_mood_desc: "حمّل لوحة مزاجية جاهزة إن وجدت",
    upload_logo: "شعار العلامة التجارية",
    upload_logo_desc: "حمّل شعار علامتك أو هويتك البصرية",
    upload_ref: "تصميم مرجعي",
    upload_ref_desc: "حمّل مساحات مرجعية تعجبك",
    upload_logo_co: "شعار الشركة",
    upload_logo_co_desc: "حمّل شعار شركتك أو دليل الهوية",
    choose_image: "اختر صورة",
    upload_note: "سيتم ربط تحليل الصور لاحقاً.",

    business_type: "نوع النشاط التجاري",
    brand_name: "اسم العلامة التجارية",
    brand_colors: "ألوان العلامة التجارية",
    target_customers: "الفئة المستهدفة",
    zones_title: "المناطق المطلوبة",
    zone_reception: "استقبال",
    zone_waiting: "منطقة انتظار",
    zone_display: "منطقة عرض",
    zone_seating: "منطقة جلوس",
    zone_cashier: "كاشير",
    zone_storage: "تخزين",
    zone_photo: "منطقة تصوير",
    zone_desks: "مكاتب",
    zone_meeting: "طاولة اجتماعات",
    zone_waiting_seats: "مقاعد انتظار",
    zone_presentation: "شاشة عرض",
    zone_coffee: "ركن القهوة",

    company_label: "الشركة / المؤسسة",
    employees_label: "عدد الموظفين / المستخدمين",
    work_style_title: "أسلوب العمل",
    work_style_label: "أسلوب المكتب",

    guest_type: "نوع الضيوف المستهدفين",
    guest_business: "رجال أعمال",
    guest_luxury: "ضيوف فاخرون",

    notes_title: "ملاحظات إضافية",

    res_form_title: "تفاصيل التصميم السكني",
    res_form_sub: "أخبر هندستنا عن المساحة السكنية التي تريد تصميمها.",
    com_form_title: "تفاصيل التصميم التجاري",
    com_form_sub: "أخبر هندستنا عن متطلبات مساحتك التجارية.",
    adm_form_title: "تفاصيل التصميم الإداري",
    adm_form_sub: "أخبر هندستنا عن متطلبات مساحة عملك.",
    hos_form_title: "تفاصيل التصميم الفندقي / السياحي",
    hos_form_sub: "أخبر هندستنا عن متطلبات مساحتك الفندقية.",

    results_eyebrow: "مفهوم التصميم جاهز",
    results_title: "مفهوم التصميم المولّد",
    result_img_label: "الصورة المقترحة للتصميم",
    result_img_note: "ستظهر الصورة هنا بعد ربط الـ API.",
    design_summary: "ملخص التصميم",
    sum_type: "نوع المشروع",
    sum_style: "توجه الأسلوب",
    sum_mood: "الجو العام",
    sum_mood_val: "هادئ، دافئ، وظيفي",
    sum_palette: "لوحة الألوان",
    sum_materials: "الخامات",
    sum_materials_val: "خشب طبيعي · كتان · سيراميك غير لامع",
    sum_lighting: "الإضاءة",
    sum_lighting_val: "LED مخفية دافئة + إضاءة معلقة",
    sum_furniture: "الأثاث",
    sum_furniture_val: "سرير · مكتب صغير · خزانة كبيرة",
    res_brief_title: "ملخص التصميم",
    res_brief_body:
      "ستُصمَّم المساحة بتوجه عصري هادئ يركز على الوظيفية والتناسق البصري والإضاءة الدافئة والخامات التي تتناسب مع أسلوب حياة العميل وتفضيلاته.",
    res_palette_title: "لوحة الألوان",
    res_materials_title: "الخامات",
    res_materials_list: null,
    res_furniture_title: "مقترحات الأثاث",
    res_furniture_list: null,
    res_lighting_title: "مقترحات الإضاءة",
    res_lighting_list: null,
    res_prompt_title: "برومبت توليد الصورة",
    res_prompt_body:
      "أنشئ تصيير واقعي لغرفة نوم بأسلوب Japandi الهادئ. أرضية خشب بلوط طبيعي، ستائر كتان، أسقف LED مخفية دافئة، سرير منخفض، مكتب عائم صغير بالقرب من النافذة، خزانة مدمجة بمقابض نحاسية. لوحة ألوان: بيج، أبيض مائل، أخشاب دافئة، لمسات زيتي. إضاءة دافئة ناعمة 2700 كلفن. أسلوب تصوير داخلي فوتوريالستيك احترافي.",
    copy_btn: "نسخ البرومبت",
    edit_btn: "تعديل المتطلبات",
    new_design_btn: "+ ابدأ تصميم جديد",
    pdf_btn: "⬇ تحميل ملف PDF",
    footer_tagline: "مساعد ذكي للتصميم الداخلي للمصممين المحترفين.",
    footer_copy: "© 2025 هندستنا. مصمم لمهندسي الديكور والمعماريين.",
  },
};

/* ============================================================
   STATE
   ============================================================ */
let currentLang = "en";
let currentSection = "home";
let selectedType = null;
let previousFormId = null;
const API_BASE =
  window.location.hostname === "127.0.0.1" ||
  window.location.hostname === "localhost"
    ? "http://127.0.0.1:5000"
    : "";

/* ============================================================
   LIGHTING HTML BUILDER
   ============================================================ */
function buildLightingHTML(suffix) {
  const t = translations[currentLang];
  return `
    <div class="lighting-section">
      <div class="form-grid">
        <div class="field-group">
          <label>${t.light_purpose}</label>
          <select name="lightPurpose_${suffix}">
            <option value="">${t.light_purpose_ph}</option>
            <option>${t.light_functional}</option>
            <option>${t.light_mood}</option>
            <option>${t.light_decorative}</option>
            <option>${t.light_display}</option>
            <option>${t.light_relaxing}</option>
            <option>${t.light_work}</option>
          </select>
        </div>
        <div class="field-group">
          <label>${t.light_natural}</label>
          <select name="naturalLight_${suffix}">
            <option value="">${t.light_natural_ph}</option>
            <option>${t.light_strong}</option>
            <option>${t.light_medium}</option>
            <option>${t.light_weak}</option>
            <option>${t.light_none}</option>
          </select>
        </div>
        <div class="field-group">
          <label>${t.light_temp}</label>
          <select name="lightTemp_${suffix}">
            <option value="">${t.light_temp_ph}</option>
            <option>${t.light_warm}</option>
            <option>${t.light_neutral}</option>
            <option>${t.light_cool}</option>
          </select>
        </div>
      </div>

      <div class="field-group" style="margin-top:8px;">
        <label>${t.light_fixtures}</label>
        <p style="font-size:.78rem;color:var(--muted);margin-bottom:10px;">${t.light_fixture_note}</p>
        <div class="checkbox-grid">
          <label class="check-item"><input type="checkbox" name="fixtures_${suffix}" value="LED" /><span>${t.light_led}</span></label>
          <label class="check-item"><input type="checkbox" name="fixtures_${suffix}" value="Spotlights" /><span>${t.light_spot}</span></label>
          <label class="check-item"><input type="checkbox" name="fixtures_${suffix}" value="Pendant" /><span>${t.light_pendant}</span></label>
          <label class="check-item"><input type="checkbox" name="fixtures_${suffix}" value="Chandelier" /><span>${t.light_chandelier}</span></label>
          <label class="check-item"><input type="checkbox" name="fixtures_${suffix}" value="Sconce" /><span>${t.light_sconce}</span></label>
          <label class="check-item"><input type="checkbox" name="fixtures_${suffix}" value="Floor Lamp" /><span>${t.light_floor}</span></label>
          <label class="check-item"><input type="checkbox" name="fixtures_${suffix}" value="Table Lamp" /><span>${t.light_table}</span></label>
          <label class="check-item"><input type="checkbox" name="fixtures_${suffix}" value="Track" /><span>${t.light_track}</span></label>
        </div>
      </div>

      <div class="lighting-hint">${t.light_hint}</div>
    </div>
  `;
}

function injectLightingContent() {
  const ids = ["res", "com", "adm", "hos"];
  ids.forEach((id) => {
    const el = document.getElementById(`lighting-${id}-content`);
    if (el) el.innerHTML = buildLightingHTML(id);
  });
}

/* ============================================================
   SECTION NAVIGATION
   ============================================================ */
function showSection(id) {
  document
    .querySelectorAll(".section")
    .forEach((s) => s.classList.remove("active"));
  const target = document.getElementById(id);
  if (target) {
    target.classList.add("active");
    currentSection = id;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
  closeMobileMenu();
}

/* ============================================================
   PROJECT TYPE SELECTION
   ============================================================ */
function selectType(type) {
  selectedType = type;
  const formId = `form-${type}`;
  previousFormId = formId;
  showSection(formId);
}

/* ============================================================
   LEGACY PREVIEW SUBMISSION
   ============================================================ */
function submitFormPreviewOnly(e) {
  e.preventDefault();
  const form = e.target;
  const nameEl = form.querySelector('[name="projectName"]');

  if (nameEl && !nameEl.value.trim()) {
    nameEl.focus();
    showToast(
      currentLang === "ar"
        ? "من فضلك أدخل اسم المشروع."
        : "Please enter a project name.",
    );
    return;
  }

  // Update result summary with project name & type
  const resTypeEl = document.getElementById("res-type");
  if (resTypeEl) {
    const typeName = selectedType
      ? translations[currentLang][`type_${selectedType.substring(0, 3)}`] ||
        selectedType
      : "Design Project";
    const spaceEl =
      form.querySelector('[name="spaceType"]') ||
      form.querySelector('[name="businessType"]');
    const spaceName = spaceEl ? spaceEl.value : "";
    resTypeEl.textContent = spaceName ? `${typeName} — ${spaceName}` : typeName;
  }

  showSection("results");
  showToast(
    currentLang === "ar"
      ? "✦ تم توليد مفهوم التصميم!"
      : "✦ Design concept generated!",
  );
}

/* ============================================================
   API FORM SUBMISSION
   ============================================================ */
function getProjectTypeFromForm(form) {
  const section = form.closest(".section");
  if (!section || !section.id) return selectedType || "design";
  return section.id.replace("form-", "") || selectedType || "design";
}

function normalizeFieldName(name) {
  return name.replace(/_(res|com|adm|hos)$/i, "");
}

function cleanValue(value) {
  if (typeof value !== "string") return value;
  const trimmed = value.trim();
  return trimmed ? trimmed : null;
}

function collectFormData(form) {
  const data = {
    projectType: getProjectTypeFromForm(form),
    language: currentLang,
  };
  const grouped = {};
  const fieldMap = {
    prefColors: "preferredColors",
    avoidColors: "colorsToAvoid",
    furniture: "furnitureRequirements",
    inspiration: "personalInspiration",
    condition: "currentCondition",
  };

  form.querySelectorAll("input, select, textarea").forEach((field) => {
    if (!field.name || field.disabled) return;
    const rawName = normalizeFieldName(field.name);
    const name = fieldMap[rawName] || rawName;

    if (field.type === "file") {
      if (field.files && field.files.length) {
        data.uploads = data.uploads || {};
        data.uploads[name] = Array.from(field.files).map((file) => ({
          name: file.name,
          type: file.type || "not specified",
          size: file.size,
        }));
      }
      return;
    }

    if (field.type === "checkbox") {
      if (field.checked) {
        grouped[name] = grouped[name] || [];
        grouped[name].push(field.value);
      }
      return;
    }

    const value = cleanValue(field.value);
    if (value !== null) data[name] = value;
  });

  Object.keys(grouped).forEach((name) => {
    if (name === "fixtures") {
      data.lighting = data.lighting || {};
      data.lighting.fixtures = grouped[name];
    } else {
      data[name] = grouped[name];
    }
  });

  const lightingMap = {
    lightPurpose: "purpose",
    naturalLight: "natural_light",
    lightTemp: "temperature",
  };

  Object.keys(lightingMap).forEach((source) => {
    if (data[source]) {
      data.lighting = data.lighting || {};
      data.lighting[lightingMap[source]] = data[source];
      delete data[source];
    }
  });

  if (!data.uploads) {
    data.uploads = {
      status: "placeholder_only",
      imagesProvided: false,
      note: "Upload UI exists, but no image file was submitted.",
    };
  }

  return data;
}

function setSubmitLoading(button, isLoading) {
  if (!button) return;
  if (isLoading) {
    button.dataset.originalText = button.textContent;
    button.disabled = true;
    button.textContent = "Generating your design concept...";
  } else {
    button.disabled = false;
    button.textContent =
      button.dataset.originalText || translations[currentLang].generate_btn;
  }
}

function textOrFallback(value) {
  if (Array.isArray(value)) return value.filter(Boolean).join(", ");
  return value || "Not specified";
}

function updateText(selector, value) {
  const el = document.querySelector(selector);
  if (el) el.textContent = textOrFallback(value);
}

function renderList(selector, items, mapper) {
  const el = document.querySelector(selector);
  if (!el) return;
  const values = Array.isArray(items) ? items : [];
  el.innerHTML = "";
  values.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = mapper ? mapper(item) : String(item);
    el.appendChild(li);
  });
  if (!values.length) {
    const li = document.createElement("li");
    li.textContent = textOrFallback(null);
    el.appendChild(li);
  }
}

function ensureDynamicDetailCard(id, title, listMode) {
  let card = document.getElementById(id);
  if (card) return card;

  const grid = document.querySelector(".result-details-grid");
  if (!grid) return null;

  card = document.createElement("div");
  card.className = "detail-card";
  card.id = id;

  const icon = document.createElement("div");
  icon.className = "detail-card-icon";
  icon.textContent = "*";

  const heading = document.createElement("h4");
  heading.textContent = title;

  const body = document.createElement(listMode ? "ul" : "p");
  if (listMode) body.className = "detail-list";

  card.appendChild(icon);
  card.appendChild(heading);
  card.appendChild(body);
  grid.insertBefore(card, grid.querySelector(".prompt-card"));
  return card;
}

function renderDynamicTextCard(id, title, value) {
  const card = ensureDynamicDetailCard(id, title, false);
  if (!card) return;
  const body = card.querySelector("p");
  if (body) body.textContent = textOrFallback(value);
}

function renderDynamicListCard(id, title, items) {
  const card = ensureDynamicDetailCard(id, title, true);
  if (!card) return;
  const list = card.querySelector("ul");
  if (!list) return;
  list.innerHTML = "";
  const values = Array.isArray(items) ? items : [];
  values.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = String(item);
    list.appendChild(li);
  });
  if (!values.length) {
    const li = document.createElement("li");
    li.textContent = textOrFallback(null);
    list.appendChild(li);
  }
}

function safeHex(hex, fallback) {
  return /^#[0-9a-f]{6}$/i.test(hex || "") ? hex : fallback;
}

function renderPalette(colors) {
  const palette = Array.isArray(colors) ? colors : [];
  const names = palette
    .map((color) => color.name)
    .filter(Boolean)
    .join(", ");
  const summaryDots = document.querySelectorAll(".palette-val .dot");
  const fallbacks = ["#E8DCCB", "#FFFBF3", "#C4A07D", "#6B7A5C", "#1E3A5F"];

  summaryDots.forEach((dot, index) => {
    const color = palette[index];
    dot.style.background = safeHex(
      color && color.hex,
      fallbacks[index] || "#D8D1C7",
    );
    dot.style.display = color ? "inline-block" : "none";
  });

  const namesEl = document.querySelector(".palette-names");
  if (namesEl) namesEl.textContent = names || textOrFallback(null);

  const swatches = document.querySelector(".palette-swatches");
  if (!swatches) return;
  swatches.innerHTML = "";
  palette.forEach((color, index) => {
    const swatch = document.createElement("div");
    swatch.className = "swatch";
    swatch.style.background = safeHex(color.hex, fallbacks[index] || "#D8D1C7");
    const label = document.createElement("span");
    label.textContent = color.name || color.usage || "Color";
    swatch.appendChild(label);
    swatches.appendChild(swatch);
  });
}

function renderSuggestedImage(result) {
  const img = document.querySelector(".result-img-wrap img");
  const placeholder = document.querySelector(".result-img-placeholder");
  const note = document.querySelector(".result-img-label small");

  if ((result.image_base64 || result.image_url) && img) {
    img.onerror = () => {
      console.error("Generated image data or URL failed to load.");
      img.style.display = "none";
      if (placeholder) placeholder.style.display = "flex";
      if (note) {
        note.textContent =
          "An image was generated, but it could not be displayed. Please try again.";
      }
    };
    img.onload = () => {
      img.style.display = "block";
      if (placeholder) placeholder.style.display = "none";
    };

    // Prioritize base64, fallback to URL.
    img.src = result.image_base64
      ? `data:${result.image_mime_type || "image/jpeg"};base64,${
          result.image_base64
        }`
      : result.image_url;

    img.style.display = "block";
    if (placeholder) placeholder.style.display = "none";
    return;
  }

  // This block runs if no image data/URL was provided at all.
  if (img) img.style.display = "none";
  if (placeholder) placeholder.style.display = "flex";
  if (note) {
    if (result.image_generation_status === "failed") {
      // Use the specific error from the backend if available
      note.textContent =
        result.image_generation_error ||
        "Image generation failed. You can still use the prompt below.";
    } else {
      note.textContent =
        "Suggested image will be generated here after image model integration.";
    }
  }
}

function renderUnavailableState(message) {
  const friendlyMessage =
    message ||
    "Gemini is temporarily unavailable. Please try again in a few minutes.";
  showSection("results");
  renderSuggestedImage({});
  updateText("#res-type", "Design concept unavailable");

  const summaryVals = document.querySelectorAll(
    ".result-summary-card .sum-val",
  );
  summaryVals.forEach((el, index) => {
    if (index !== 0) el.textContent = "Not available";
  });

  const detailCards = document.querySelectorAll(
    ".result-details-grid .detail-card",
  );
  if (detailCards[0]) {
    const brief = detailCards[0].querySelector("p");
    if (brief) brief.textContent = friendlyMessage;
  }

  renderPalette([]);
  renderList('[data-i18n="res_materials_list"]', []);
  renderList('[data-i18n="res_furniture_list"]', []);
  renderList('[data-i18n="res_lighting_list"]', []);
  renderDynamicTextCard(
    "concept-summary-card",
    "Concept Summary",
    friendlyMessage,
  );
  renderDynamicListCard("layout-suggestions-card", "Layout Suggestions", []);
  renderDynamicTextCard("image-status-card", "Image Status", friendlyMessage);

  const promptText = document.getElementById("prompt-text");
  if (promptText) promptText.textContent = friendlyMessage;
  showToast(friendlyMessage);
}

function renderDesignResult(result) {
  const summaryVals = document.querySelectorAll(
    ".result-summary-card .sum-val",
  );
  const materials = Array.isArray(result.materials) ? result.materials : [];
  const furniture = Array.isArray(result.furniture_suggestions)
    ? result.furniture_suggestions
    : [];
  const lighting = Array.isArray(result.lighting_suggestions)
    ? result.lighting_suggestions
    : [];

  updateText(
    "#res-type",
    `${textOrFallback(result.project_type)} - ${textOrFallback(result.space_type)}`,
  );
  if (summaryVals[1])
    summaryVals[1].textContent = textOrFallback(result.style_direction);
  if (summaryVals[2]) summaryVals[2].textContent = textOrFallback(result.mood);
  if (summaryVals[4])
    summaryVals[4].textContent =
      materials
        .map((item) => item.name || item.usage || item)
        .filter(Boolean)
        .join(" - ") || textOrFallback(null);
  if (summaryVals[5])
    summaryVals[5].textContent =
      lighting.slice(0, 2).join(" + ") || textOrFallback(null);
  if (summaryVals[6])
    summaryVals[6].textContent =
      furniture.slice(0, 3).join(" - ") || textOrFallback(null);

  const detailCards = document.querySelectorAll(
    ".result-details-grid .detail-card",
  );
  if (detailCards[0]) {
    const brief = detailCards[0].querySelector("p");
    if (brief)
      brief.textContent = textOrFallback(
        result.design_brief || result.concept_summary,
      );
  }

  renderPalette(result.color_palette);
  renderList(
    '[data-i18n="res_materials_list"]',
    materials,
    (item) => `${item.name || "Material"}: ${item.usage || "Suggested use"}`,
  );
  renderList('[data-i18n="res_furniture_list"]', furniture);
  renderList('[data-i18n="res_lighting_list"]', lighting);
  renderDynamicTextCard(
    "concept-summary-card",
    "Concept Summary",
    result.concept_summary,
  );
  renderDynamicListCard(
    "layout-suggestions-card",
    "Layout Suggestions",
    result.layout_suggestions,
  );
  renderDynamicTextCard(
    "image-status-card",
    "Image Status",
    result.image_generation_status === "failed"
      ? result.image_generation_error || "Image generation failed."
      : result.image_generation_status || "Not requested",
  );
  renderDynamicTextCard(
    "image-provider-card",
    "Image Provider",
    result.image_provider || "Not specified",
  );
  renderDynamicTextCard(
    "negative-prompt-card",
    "Negative Prompt",
    result.negative_prompt || "Not specified",
  );
  renderDynamicTextCard(
    "image-url-prompt-card",
    "Image URL Prompt (for Pollinations)",
    result.image_url_prompt || "Not generated",
  );
  renderDynamicTextCard(
    "concept-status-card",
    "Concept Generation Status",
    result.concept_generation_status || "Not specified",
  );

  const promptText = document.getElementById("prompt-text");
  if (promptText)
    promptText.textContent = textOrFallback(result.image_generation_prompt);

  renderSuggestedImage(result);
}

function showResultError(message) {
  showSection("results");
  const promptText = document.getElementById("prompt-text");
  if (promptText) promptText.textContent = message;
  const detailCards = document.querySelectorAll(
    ".result-details-grid .detail-card",
  );
  if (detailCards[0]) {
    const brief = detailCards[0].querySelector("p");
    if (brief) brief.textContent = message;
  }
  showToast(message);
}

async function submitForm(e) {
  e.preventDefault();
  const form = e.target;
  const nameEl = form.querySelector('[name="projectName"]');
  const submitButton = form.querySelector('[type="submit"]');

  if (nameEl && !nameEl.value.trim()) {
    nameEl.focus();
    showToast("Please enter a project name.");
    return;
  }

  const payload = collectFormData(form);
  const requiredSpace =
    payload.spaceType ||
    payload.businessType ||
    payload.space_type ||
    payload.business_type;
  if (!requiredSpace) {
    showToast("Please choose the space or business type.");
    return;
  }

  setSubmitLoading(submitButton, true);
  console.log("Hendsetna payload sent to backend:", payload);

  try {
    const response = await fetch(`${API_BASE}/api/generate-design`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const result = await response.json().catch(() => ({}));
    console.log("Hendsetna backend response:", result);
    console.log(
      "Final image prompt:",
      result.image_generation_prompt || "Not generated",
    );
    console.log(
      "Image status:",
      result.image_generation_status || "Not generated",
    );
    if (result.success === false || result.error_type) {
      renderUnavailableState(result.error);
      return;
    }

    if (!response.ok) {
      throw new Error(result.error || "Backend request failed.");
    }

    renderDesignResult(result);
    showSection("results");
    showToast("Design concept generated!");
  } catch (error) {
    showResultError(
      "Sorry, Hendsetna could not generate the concept right now. Please check the backend and try again.",
    );
  } finally {
    setSubmitLoading(submitButton, false);
  }
}

/* ============================================================
   DEMO RESULT
   ============================================================ */
function loadDemoAndShow() {
  selectedType = "residential";
  previousFormId = "form-residential";
  const resTypeEl = document.getElementById("res-type");
  if (resTypeEl)
    resTypeEl.textContent =
      translations[currentLang].sp_bedroom || "Residential Bedroom";
  showSection("results");
}

/* ============================================================
   EDIT REQUIREMENTS (back to last form)
   ============================================================ */
function editRequirements() {
  if (previousFormId) {
    showSection(previousFormId);
  } else {
    showSection("project-types");
  }
}

/* ============================================================
   COPY PROMPT
   ============================================================ */
function copyPrompt() {
  const promptText = document.getElementById("prompt-text");
  if (!promptText) return;
  const text = promptText.textContent || promptText.innerText;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => {
      showToast(
        currentLang === "ar"
          ? "تم نسخ البرومبت!"
          : "Prompt copied to clipboard!",
      );
    });
  } else {
    // Fallback
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    showToast(
      currentLang === "ar" ? "تم نسخ البرومبت!" : "Prompt copied to clipboard!",
    );
  }
}

/* ============================================================
   TOAST NOTIFICATION
   ============================================================ */
function showToast(message) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 2800);
}

/* ============================================================
   LANGUAGE TOGGLE
   ============================================================ */
function toggleLanguage() {
  currentLang = currentLang === "en" ? "ar" : "en";
  applyLanguage();
}

function applyLanguage() {
  const t = translations[currentLang];
  const body = document.body;
  const langBtn = document.getElementById("lang-btn");

  // Direction
  if (currentLang === "ar") {
    body.classList.add("rtl");
    document.documentElement.setAttribute("lang", "ar");
    document.documentElement.setAttribute("dir", "rtl");
    if (langBtn) langBtn.textContent = "English";
  } else {
    body.classList.remove("rtl");
    document.documentElement.setAttribute("lang", "en");
    document.documentElement.setAttribute("dir", "ltr");
    if (langBtn) langBtn.textContent = "العربية";
  }

  // Translate all data-i18n elements
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (t[key] !== undefined && t[key] !== null) {
      el.textContent = t[key];
    }
  });

  // Translate placeholders
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (t[key]) el.setAttribute("placeholder", t[key]);
  });

  // Rebuild lighting sections with new language
  injectLightingContent();
}

/* ============================================================
   MOBILE MENU
   ============================================================ */
function toggleMobileMenu() {
  const links = document.getElementById("nav-links");
  if (links) links.classList.toggle("mobile-open");
}
function closeMobileMenu() {
  const links = document.getElementById("nav-links");
  if (links) links.classList.remove("mobile-open");
}

/* ============================================================
   NAVBAR SCROLL EFFECT
   ============================================================ */
window.addEventListener(
  "scroll",
  () => {
    const navbar = document.getElementById("navbar");
    if (!navbar) return;
    if (window.scrollY > 10) {
      navbar.style.boxShadow = "0 4px 24px rgba(30,58,95,0.12)";
    } else {
      navbar.style.boxShadow = "";
    }
  },
  { passive: true },
);

/* ============================================================
   INIT
   ============================================================ */
document.addEventListener("DOMContentLoaded", () => {
  injectLightingContent();
  applyLanguage(); // Ensure initial state is correct

  // Show placeholder images that fail to load
  document
    .querySelectorAll(".result-img-placeholder")
    .forEach((el) => (el.style.display = "flex"));

  // Show home section
  showSection("home");
});
