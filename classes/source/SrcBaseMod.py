main = """package <package>;


<imports>

@Mod(modid = <classname>.MODID, name = "<name>", version = <classname>.VERSION)

public class <classname> {

    public static final String MODID = "<modid>";
    public static final String VERSION = "<version>";
    
    @Instance(MODID)
    public static <classname> instance;
    
    <proxies>


    //declarations
    <declarations>
   
    public static void registerEntity(Class entityClass, int entityID, String name) {
        EntityRegistry.registerGlobalEntityID(entityClass, name, entityID);
    }
    
    public static void registerSpawnEgg(int entityID, int primaryColor, int secondaryColor) {
        EntityList.entityEggs.put(Integer.valueOf(entityID), new EntityList.EntityEggInfo(entityID, primaryColor, secondaryColor));
    }
	
	
	@EventHandler
	public void preInit(FMLPreInitializationEvent event) {
<preInit>
	}

	@EventHandler
	public void init(FMLInitializationEvent event) {
<commonInit>
		if (event.getSide() == Side.CLIENT) {
			<clientInit>
		}
	}

	@EventHandler
	public static void postInit(FMLPostInitializationEvent event) {
<postInit>
	}
}"""

imports = """import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.Mod.EventHandler;
import net.minecraftforge.fml.common.Mod.Instance;
import net.minecraftforge.fml.common.SidedProxy;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.registry.EntityRegistry;
import net.minecraftforge.fml.common.registry.GameRegistry;
import net.minecraft.entity.EntityList;
import net.minecraft.item.Item;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraft.client.renderer.entity.RenderItem;
import net.minecraft.client.Minecraft;
import net.minecraft.client.resources.model.ModelResourceLocation;"""

proxies = """"""