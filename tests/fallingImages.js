var myScale = 110
var myBlogJson = JSON.parse('{}')
var myBlogImages = new Map();


var embox2dTest_fallingImages = function() {
}

embox2dTest_fallingImages.prototype.setNiceViewCenter = function() {
    PTM = 32;
    setViewCenterWorld( new b2Vec2(0,0), true );
}

embox2dTest_fallingImages.prototype.setup = function() {

    var NUMRANGE = [];    
    while (NUMRANGE.length < 10)
        NUMRANGE.push(NUMRANGE.length+1);
    bodies = [null]; // Indexes start from 1
    
    var bd_ground = new b2BodyDef();
    var groundBody = world.CreateBody(bd_ground);

    //ground edges
    var shape0 = new b2EdgeShape();
    shape0.Set(new b2Vec2(-40.0, -6.0), new b2Vec2(40.0, -6.0));
    groundBody.CreateFixture(shape0, 0.0);
    shape0.Set(new b2Vec2(-9.0, -6.0), new b2Vec2(-9.0, -4.0));
    groundBody.CreateFixture(shape0, 0.0);
    shape0.Set(new b2Vec2(9.0, -6.0), new b2Vec2(9.0, -4.0));
    groundBody.CreateFixture(shape0, 0.0);

    var cshape = new b2CircleShape();
    cshape.set_m_radius(0.5);

    //falling shapes
    var ZERO = new b2Vec2(0, 0);
    var temp = new b2Vec2(0, 0);
    NUMRANGE.forEach(function(i) {
        var bd = new b2BodyDef();
        // bd.set_type(b2_dynamicBody);
        bd.set_type(Module.b2_dynamicBody);
        bd.set_position(ZERO);
        var body = world.CreateBody(bd);
        var randomValue = Math.random();
        if ( randomValue < 0.2 )
            body.CreateFixture(cshape, 1.0);
        else
            body.CreateFixture(createRandomPolygonShape(0.5), 1.0);
        temp.Set(16*(Math.random()-0.5), 4.0 + 2.5*i);
        body.SetTransform(temp, 0.0);
        body.SetLinearVelocity(ZERO);
        body.SetAwake(1);
        body.SetActive(1);
    });

    // //static polygon and chain shapes
    // {
    //     var verts = [];
    //     verts.push( new b2Vec2( 7,-1) );
    //     verts.push( new b2Vec2( 8,-2) );
    //     verts.push( new b2Vec2( 9, 3) );
    //     verts.push( new b2Vec2( 7, 1) );
    //     var polygonShape = createPolygonShape(verts);
    //     groundBody.CreateFixture(polygonShape, 0.0);
        
    //     //mirror vertices in x-axis and use for chain shape
    //     for (var i = 0; i < verts.length; i++)
    //         verts[i].set_x( -verts[i].get_x() );
    //     verts.reverse();
    //     var chainShape = createChainShape(verts, true);//true for closed loop *** some problem with this atm
    //     // polygonShape = createPolygonShape(verts);
    //     groundBody.CreateFixture(chainShape, 0.0);
    // }

    initMyBlog('blogJsonFile.txt')
}

function addImageBody(id) {
    var image = new Image()
    image.src = 'images/' + id + '.png'
    image.onload = function() {
        var w = image.width / myScale
        var h = image.height / myScale
        var ZERO = new b2Vec2(0, 0);
        var temp = new b2Vec2(0, 0);
        var bd = new b2BodyDef();
        // bd.set_type(b2_dynamicBody);
        bd.set_type(Module.b2_dynamicBody);
        bd.set_position(ZERO);
        var body = world.CreateBody(bd);
        var randomValue = Math.random();

        var shape = new b2PolygonShape();
        shape.SetAsBox(w / 2, h / 2);
        body.CreateFixture(shape, 1);

        temp.Set(16*(Math.random()-0.5), 4.0 + 2.5);
        body.SetTransform(temp, 0.0);
        body.SetLinearVelocity(ZERO);
        // body.SetAngle
        body.SetAwake(1);
        body.SetActive(1);

        body.SetUserData(id);
        myBlogImages.set(id, image)
        console.log(id + ' ' + image.width + ' ' + image.height);
    }
}

function initMyBlog(file) {
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                handleJsonStr(allText);
            }
        }
    }
    rawFile.send(null);
}


function handleJsonStr(str) {
    var arr = str.split("\n");
    for (i = 0; i < arr.length; i++) {
        if (arr[i].length <= 2) {
            continue
        }
        var json = JSON.parse(arr[i]);
        for (j = 0; j < json.length; j++) {
            var data = json[j].object.data
            var id = data.id
            myBlogJson[id] = data
            console.log(data.title);
            addImageBody(id);

            var title = data.title
            var time = data.first_shared_at
            var slug = data.slug
        }
        // if (i > 1) {
        //     break
        // }
    }
}